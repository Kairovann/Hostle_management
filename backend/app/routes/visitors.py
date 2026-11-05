# Visitors coming to meet students.

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from database import get_rows, get_row, change_data, find_or_404, blank_to_none, find_student_by_name

router = APIRouter(prefix="/visitors", tags=["Visitors"])

# The frontend wants: id, visitorName, student, relation, phone, visitDate, inTime, outTime
VISITOR_SELECT = """
    SELECT v.visitor_id AS id, v.visitor_name AS visitorName, s.student_name AS student,
           v.relation, v.phone, v.visit_date AS visitDate,
           TIME_FORMAT(v.check_in, '%H:%i') AS inTime,
           TIME_FORMAT(v.check_out, '%H:%i') AS outTime
    FROM visitors v
    JOIN students s ON s.student_id = v.student_id
"""


class VisitorData(BaseModel):
    visitorName: Optional[str] = None
    student: Optional[str] = None
    relation: Optional[str] = None
    phone: Optional[str] = None
    visitDate: Optional[str] = None
    inTime: Optional[str] = None
    outTime: Optional[str] = None   # may be empty = visitor has not left yet


@router.get("")
def list_visitors():
    # GET /visitors
    return get_rows(VISITOR_SELECT + " ORDER BY v.visit_date DESC, v.visitor_id DESC")


@router.post("")
def add_visitor(data: VisitorData):
    # POST /visitors
    student = find_student_by_name(data.student)
    if not data.visitDate or not data.inTime:
        raise HTTPException(status_code=400, detail="Visit date and in time are required.")
    change_data(
        "INSERT INTO visitors (student_id, visitor_name, relation, phone, visit_date, check_in, check_out) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (student["student_id"], data.visitorName, blank_to_none(data.relation),
         blank_to_none(data.phone), data.visitDate, data.inTime, blank_to_none(data.outTime)),
    )
    return {"message": "Visitor recorded"}


@router.put("/{visitor_id}")
def edit_visitor(visitor_id: int, data: VisitorData):
    # PUT /visitors/3
    find_or_404("visitors", "visitor_id", visitor_id)
    student = find_student_by_name(data.student)
    change_data(
        "UPDATE visitors SET student_id = %s, visitor_name = %s, relation = %s, phone = %s, visit_date = %s, check_in = %s, check_out = %s WHERE visitor_id = %s",
        (student["student_id"], data.visitorName, blank_to_none(data.relation),
         blank_to_none(data.phone), data.visitDate, data.inTime,
         blank_to_none(data.outTime), visitor_id),
    )
    return {"message": "Visitor updated"}


@router.delete("/{visitor_id}")
def delete_visitor(visitor_id: int):
    # DELETE /visitors/3
    find_or_404("visitors", "visitor_id", visitor_id)
    change_data("DELETE FROM visitors WHERE visitor_id = %s", (visitor_id,))
    return {"message": "Visitor deleted"}
