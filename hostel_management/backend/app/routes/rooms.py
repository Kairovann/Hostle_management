# Everything about rooms: list them, add one, edit one, delete one.
#
# The frontend sends/receives fields like "roomNumber" and "occupied",
# but the database uses "room_number" etc. The SQL below uses AS to
# rename the columns, so the frontend gets exactly what it expects.

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from database import get_rows, get_row, change_data, find_or_404, blank_to_none, refresh_room_status

router = APIRouter(prefix="/rooms", tags=["Rooms"])

# This query also counts how many students currently live in each room.
# That count is returned as "occupied", which is the name the frontend wants.
ROOM_SELECT = """
    SELECT r.room_id AS id, r.room_number AS roomNumber, r.building,
           r.room_type AS type, r.capacity, r.status,
           (SELECT COUNT(*) FROM room_allocations a
             WHERE a.room_id = r.room_id AND a.checkout_date IS NULL) AS occupied
    FROM rooms r
"""


class RoomData(BaseModel):
    # Optional = the frontend does not have to send it.
    # Every value defaults to None (empty) if it is missing.
    roomNumber: Optional[str] = None
    building: Optional[str] = None
    type: Optional[str] = None
    capacity: Optional[int] = None
    occupied: Optional[int] = None   # we calculate this ourselves, so we ignore it
    status: Optional[str] = None


@router.get("")
def list_rooms():
    # GET /rooms  ->  return every room
    return get_rows(ROOM_SELECT + " ORDER BY r.room_number")


@router.get("/{room_id}")
def get_one_room(room_id: int):
    # GET /rooms/5  ->  return one room (or a "not found" error)
    room = get_row(ROOM_SELECT + " WHERE r.room_id = %s", (room_id,))
    if room is None:
        find_or_404("rooms", "room_id", room_id)  # this raises the 404 error
    return room


@router.post("")
def add_room(data: RoomData):
    # POST /rooms  ->  add a new room
    change_data(
        "INSERT INTO rooms (room_number, building, room_type, capacity, status) VALUES (%s, %s, %s, %s, %s)",
        (data.roomNumber, blank_to_none(data.building), data.type or "Single",
         data.capacity or 1, data.status or "Available"),
    )
    return {"message": "Room added"}


@router.put("/{room_id}")
def edit_room(room_id: int, data: RoomData):
    # PUT /rooms/5  ->  save the edited room
    find_or_404("rooms", "room_id", room_id)  # stop if this room does not exist

    change_data(
        "UPDATE rooms SET room_number = %s, building = %s, room_type = %s, capacity = %s, status = %s WHERE room_id = %s",
        (data.roomNumber, blank_to_none(data.building), data.type or "Single",
         data.capacity or 1, data.status or "Available", room_id),
    )

    # If the capacity changed, the room might become Full or Available again.
    refresh_room_status(room_id)
    return {"message": "Room updated"}


@router.delete("/{room_id}")
def delete_room(room_id: int):
    # DELETE /rooms/5  ->  remove the room
    find_or_404("rooms", "room_id", room_id)

    # Old allocation records for this room must go first,
    # otherwise the database refuses to delete the room.
    change_data("DELETE FROM room_allocations WHERE room_id = %s", (room_id,))
    change_data("DELETE FROM rooms WHERE room_id = %s", (room_id,))
    return {"message": "Room deleted"}
