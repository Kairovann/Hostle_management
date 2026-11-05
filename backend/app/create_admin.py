# Run this ONE time to make the first admin account:   python create_admin.py

from auth import hash_password
from database import change_data

name = input("Admin name: ")
email = input("Admin email: ")
password = input("Admin password: ")

change_data(
    "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, 'admin')",
    (name, email, hash_password(password)),
)
print("Admin created. You can login with", email)
