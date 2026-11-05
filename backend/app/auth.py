# Login helpers: password hashing, tokens, and "who is calling?" checks.

import os
import time
import bcrypt
import jwt
from fastapi import Header, Depends, HTTPException
import database  # importing this loads the .env file first

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret")


def hash_password(password):
    # Never save the real password. Save a scrambled version instead.
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password, saved_hash):
    return bcrypt.checkpw(password.encode(), saved_hash.encode())


def make_token(user_id, role):
    # A token is a signed note that says "this is user 3, an admin".
    # It stops working after 8 hours.
    data = {"user_id": user_id, "role": role, "exp": time.time() + 8 * 3600}
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def get_current_user(authorization: str = Header(default="")):
    # The frontend sends:  Authorization: Bearer <token>
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Please login first")

    token = authorization[7:]  # remove the word "Bearer "

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return data


def admin_only(user=Depends(get_current_user)):
    # Put this on any route that only the admin may use.
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user
