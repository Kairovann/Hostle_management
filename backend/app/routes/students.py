# Everything about students.
#
# A small warning: this is the longest file of the project, because one
# "student" is really TWO things:
#   1. a login account in the "users" table   (so the student can sign in)
#   2. a record in the "students" table       (course, phone, parents, etc.)
#
# When the admin adds a student we create BOTH.
# The student's login password is always "student123" (they can change it later).

from datetime import date

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from auth import hash_password
from database import (
    get_rows, get_row, change_data, find_or_404, blank_to_none,
    find_room_by_number, refresh_room_status,
)

router = APIRouter(prefix="/students", tags=["Students"])

# NOTE: the routes in this file are intentionally open (no admin_only),
# because the current frontend does not send a login token with its requests.
# Your login endpoint (/login) still works - this only affects these lists.
# To lock these routes later, add:  dependencies=[Depends(admin_only)]  to the
# APIRouter line above (and import admin_only from auth).

# This SELECT also finds the student's current room (if they have one).
# The frontend wants simple names, so we rename the columns with AS:
#   student_id  -> id
#   student_name -> name
#   room_number -> room
STUDENT_SELECT = """
    SELECT s.student_id AS id, s.student_name AS name, s.email, s.phone,
           s.course, s.year, s.status, r.room_number AS room
    FROM students s
    LEFT JOIN room_allocations a ON a.student_id = s.student_id AND a.checkout_date IS NULL
    LEFT JOIN rooms r ON r.room_id = a.room_id
"""


class StudentData(BaseModel):
    # Optional = if the frontend does not send the field, it becomes None.
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    year: Optional[str] = None
    room: Optional[str] = None      # a room number like "A-101", or empty
    status: Optional[str] = None


def get_student_or_404(student_id):
    # Find one student (with room) or stop with a "not found" error.
    student = get_row(STUDENT_SELECT + " WHERE s.student_id = %s", (student_id,))
    if student is None:
        find_or_404("students", "student_id", student_id)  # raises the 404
    return student


def move_student_to_room(student_id, room_number):
    # Give this student a room.
    # If the student already has a different room, they are checked out of it first.
    # If room_number is empty/None, the student is simply checked out.
    today = date.today().isoformat()

    # The room the student is in RIGHT NOW (if any)
    current = get_row(
        "SELECT * FROM room_allocations WHERE student_id = %s AND checkout_date IS NULL",
        (student_id,),
    )

    if room_number is None:
        # No room wanted. If the student has one, check them out.
        if current is not None:
            change_data("UPDATE room_allocations SET checkout_date = %s WHERE allocation_id = %s",
                        (today, current["allocation_id"]))
            refresh_room_status(current["room_id"])
        return

    room = find_room_by_number(room_number)  # stops with an error if the room does not exist

    if current is not None and current["room_id"] == room["room_id"]:
        return  # already in this room, nothing to do

    if room["status"] == "Full":
        raise HTTPException(status_code=400, detail="Room " + room_number + " is full.")

    # Check the student out of their old room (if they had one)
    if current is not None:
        change_data("UPDATE room_allocations SET checkout_date = %s WHERE allocation_id = %s",
                    (today, current["allocation_id"]))
        refresh_room_status(current["room_id"])

    # Check the student into the new room
    change_data(
        "INSERT INTO room_allocations (student_id, room_id, allocation_date) VALUES (%s, %s, %s)",
        (student_id, room["room_id"], today),
    )
    refresh_room_status(room["room_id"])


@router.get("")
def list_students():
    # GET /students  ->  return every student
    return get_rows(STUDENT_SELECT + " ORDER BY s.student_id")


@router.get("/{student_id}")
def get_one_student(student_id: int):
    # GET /students/3  ->  return one student
    return get_student_or_404(student_id)


@router.post("")
def add_student(data: StudentData):
    # POST /students  ->  add a new student (account + record)

    # If a room was typed, it must exist (and have space) BEFORE we create anything.
    if data.room:
        room = find_room_by_number(data.room)
        if room["status"] == "Full":
            raise HTTPException(status_code=400, detail="Room " + data.room + " is full.")

    # Emails must be unique - check first so the error message is friendly.
    existing = get_row("SELECT user_id FROM users WHERE email = %s", (data.email,))
    if existing is not None:
        raise HTTPException(status_code=400, detail="That email is already registered.")

    # 1. Create the login account (every student starts with password "student123")
    user_id = change_data(
        "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, 'student')",
        (data.name, data.email, hash_password("student123")),
    )

    # 2. Create the student record, linked to that account
    student_id = change_data(
        """INSERT INTO students (user_id, student_name, email, phone, course, year, status)
           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (user_id, data.name, data.email, blank_to_none(data.phone),
         blank_to_none(data.course), blank_to_none(data.year), data.status or "Active"),
    )

    # 3. If a room was typed, move the student into it
    if data.room:
        move_student_to_room(student_id, data.room)

    return get_student_or_404(student_id)


@router.put("/{student_id}")
def edit_student(student_id: int, data: StudentData):
    # PUT /students/3  ->  save the edited student
    student = find_or_404("students", "student_id", student_id)

    # If the email changed, make sure nobody else is using it
    clash = get_row("SELECT user_id FROM users WHERE email = %s AND user_id != %s",
                    (data.email, student["user_id"]))
    if clash is not None:
        raise HTTPException(status_code=400, detail="That email is already registered.")

    # Update the login account (name and email are stored there too)
    change_data("UPDATE users SET username = %s, email = %s WHERE user_id = %s",
                (data.name, data.email, student["user_id"]))

    # Update the student record itself
    change_data(
        """UPDATE students SET student_name = %s, email = %s, phone = %s, course = %s, year = %s, status = %s
           WHERE student_id = %s""",
        (data.name, data.email, blank_to_none(data.phone), blank_to_none(data.course),
         blank_to_none(data.year), data.status or "Active", student_id),
    )

    # Handle the room field: move them, or check them out if it was emptied
    move_student_to_room(student_id, blank_to_none(data.room))

    return get_student_or_404(student_id)


@router.delete("/{student_id}")
def delete_student(student_id: int):
    # DELETE /students/3  ->  remove the student AND their login account
    student = find_or_404("students", "student_id", student_id)

    change_data("DELETE FROM students WHERE student_id = %s", (student_id,))
    change_data("DELETE FROM users WHERE user_id = %s", (student["user_id"],))
    return {"message": "Student deleted"}
