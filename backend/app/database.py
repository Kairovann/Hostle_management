# This file talks to MariaDB.
# Every other file uses the small functions below, so SQL stays easy to read.

import os
import pymysql
from dotenv import load_dotenv
from fastapi import HTTPException

# Read the settings from the .env file
load_dotenv()


def get_db():
    # Open a connection to the database
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "hostel_db"),
        cursorclass=pymysql.cursors.DictCursor,  # rows come back like {"name": "Aarav"}
    )


def get_rows(sql, values=()):
    # Run a SELECT and return a list of rows
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(sql, values)
        return cursor.fetchall()
    except pymysql.MySQLError as error:
        raise HTTPException(status_code=400, detail="Database error: " + str(error))
    finally:
        db.close()


def get_row(sql, values=()):
    # Run a SELECT and return only the first row (or None if nothing found)
    rows = get_rows(sql, values)
    if len(rows) == 0:
        return None
    return rows[0]


def change_data(sql, values=()):
    # Run INSERT, UPDATE or DELETE. Returns the id of a newly inserted row.
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(sql, values)
        db.commit()
        return cursor.lastrowid
    except pymysql.MySQLError as error:
        raise HTTPException(status_code=400, detail="Database error: " + str(error))
    finally:
        db.close()


def find_or_404(table, id_column, id_value):
    # Find one row by id. If it does not exist, send a "not found" error.
    row = get_row("SELECT * FROM " + table + " WHERE " + id_column + " = %s", (id_value,))
    if row is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return row


def blank_to_none(value):
    # The frontend sends "" for empty fields. The database wants NULL instead.
    if value == "":
        return None
    return value


def find_student_by_name(name):
    # Many forms let the admin type a student NAME (like "Aarav Sharma").
    # This finds that student, or stops with a clear error message.
    student = get_row("SELECT * FROM students WHERE student_name = %s", (name,))
    if student is None:
        raise HTTPException(status_code=400, detail='Student "' + str(name) + '" not found. Add the student first.')
    return student


def find_room_by_number(room_number):
    # Same idea as above, but for rooms: find a room by its number (like "A-101").
    room = get_row("SELECT * FROM rooms WHERE room_number = %s", (room_number,))
    if room is None:
        raise HTTPException(status_code=400, detail='Room "' + str(room_number) + '" not found. Add the room first.')
    return room


def refresh_room_status(room_id):
    # Set the room to Full or Available depending on how many students live in it.
    # Rooms marked Maintenance are left alone.
    room = get_row("SELECT capacity, status FROM rooms WHERE room_id = %s", (room_id,))
    if room is None or room["status"] == "Maintenance":
        return

    count_row = get_row(
        "SELECT COUNT(*) AS total FROM room_allocations WHERE room_id = %s AND checkout_date IS NULL",
        (room_id,),
    )

    if count_row["total"] >= room["capacity"]:
        new_status = "Full"
    else:
        new_status = "Available"

    change_data("UPDATE rooms SET status = %s WHERE room_id = %s", (new_status, room_id))
