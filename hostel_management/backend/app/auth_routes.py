from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth import check_password, make_token
from database import get_row

router = APIRouter(tags=["Login"])


class LoginData(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(data: LoginData):
    user = get_row("SELECT * FROM users WHERE email = %s", (data.email,))

    if user is None or not check_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password.")

    # If this is a student, also send the student_id
    student_id = None
    if user["role"] == "student":
        student = get_row("SELECT student_id FROM students WHERE user_id = %s", (user["user_id"],))
        if student is not None:
            student_id = student["student_id"]

    return {
        "token": make_token(user["user_id"], user["role"]),
        "user": {
            "user_id": user["user_id"],
            "name": user["username"],
            "email": user["email"],
            "role": user["role"],
            "student_id": student_id,
        },
    }
