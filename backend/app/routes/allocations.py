# Room allocations = "which student lives in which room".
#
# The admin types student and room NAMES (like "Aarav Sharma" and "A-101"),
# so this file looks up the real ids from those names before saving.

from datetime import date

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from database import (
    get_rows, get_row, change_data, find_or_404,
    find_student_by_name, find_room_by_number, refresh_room_status,
)

router = APIRouter(prefix="/allocations", tags=["Room Allocations"])

# The frontend wants: id, student, room, date, status
# (status is "Active" while checkout_date is empty, otherwise "Ended")
ALLOCATION_SELECT = """
    SELECT a.allocation_id AS id, s.student_name AS student, r.room_number AS room,
           a.allocation_date AS date,
           IF(a.checkout_date IS NULL, 'Active', 'Ended') AS status
    FROM room_allocations a
    JOIN students s ON s.student_id = a.student_id
    JOIN rooms r ON r.room_id = a.room_id
"""


class AllocationData(BaseModel):
    student: Optional[str] = None
    room: Optional[str] = None
    date: Optional[str] = None
    status: Optional[str] = None   # "Active" or "Ended"


def current_allocation(student_id):
    # The allocation where this student still lives (checkout_date empty)
    return get_row(
        "SELECT * FROM room_allocations WHERE student_id = %s AND checkout_date IS NULL",
        (student_id,),
    )


@router.get("")
def list_allocations():
    # GET /allocations
    return get_rows(ALLOCATION_SELECT + " ORDER BY a.allocation_id DESC")


@router.post("")
def add_allocation(data: AllocationData):
    # POST /allocations
    student = find_student_by_name(data.student)
    room = find_room_by_number(data.room)
    today = date.today().isoformat()

    # One room per student: check they are not already living somewhere
    if current_allocation(student["student_id"]) is not None:
        raise HTTPException(status_code=400, detail=student["student_name"] + " already has a room. Check that student out first.")

    if room["status"] == "Full":
        raise HTTPException(status_code=400, detail="Room " + data.room + " is full.")

    checkout = None if data.status != "Ended" else today
    change_data(
        "INSERT INTO room_allocations (student_id, room_id, allocation_date, checkout_date) VALUES (%s, %s, %s, %s)",
        (student["student_id"], room["room_id"], data.date or today, checkout),
    )
    refresh_room_status(room["room_id"])
    return {"message": "Room allocated"}


@router.put("/{allocation_id}")
def edit_allocation(allocation_id: int, data: AllocationData):
    # PUT /allocations/7
    old = find_or_404("room_allocations", "allocation_id", allocation_id)

    student = find_student_by_name(data.student)
    room = find_room_by_number(data.room)
    today = date.today().isoformat()

    # If the allocation becomes "Ended", set the checkout day (today).
    # If it goes back to "Active", clear the checkout day.
    checkout = None if data.status != "Ended" else (old["checkout_date"] or today)

    change_data(
        "UPDATE room_allocations SET student_id = %s, room_id = %s, allocation_date = %s, checkout_date = %s WHERE allocation_id = %s",
        (student["student_id"], room["room_id"], data.date, checkout, allocation_id),
    )

    # The old room and the new room may both have changed Full/Available state
    refresh_room_status(old["room_id"])
    if old["room_id"] != room["room_id"]:
        refresh_room_status(room["room_id"])
    return {"message": "Allocation updated"}


@router.delete("/{allocation_id}")
def delete_allocation(allocation_id: int):
    # DELETE /allocations/7
    allocation = find_or_404("room_allocations", "allocation_id", allocation_id)
    change_data("DELETE FROM room_allocations WHERE allocation_id = %s", (allocation_id,))
    refresh_room_status(allocation["room_id"])
    return {"message": "Allocation deleted"}
