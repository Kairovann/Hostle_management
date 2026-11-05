# Complaints submitted by students.
# Students submit these from the student portal; admins update the status here.

from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from database import get_rows, get_row, change_data, find_or_404, blank_to_none, find_student_by_name

router = APIRouter(prefix="/complaints", tags=["Complaints"])

# The frontend wants: id, student, subject, description, date, status
# DATE(...) cuts the time part off, so "2026-11-05" instead of "2026-11-05 18:30:00"
COMPLAINT_SELECT = """
    SELECT c.complaint_id AS id, s.student_name AS student, c.subject, c.description,
           DATE(c.complaint_date) AS date, c.status
    FROM complaints c
    JOIN students s ON s.student_id = c.student_id
"""


class ComplaintData(BaseModel):
    student: Optional[str] = None
    subject: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    status: Optional[str] = None   # Submitted / In Progress / Resolved


@router.get("")
def list_complaints():
    # GET /complaints
    return get_rows(COMPLAINT_SELECT + " ORDER BY c.complaint_id DESC")


@router.post("")
def add_complaint(data: ComplaintData):
    # POST /complaints  (this is what the student portal form calls)
    student = find_student_by_name(data.student)
    change_data(
        "INSERT INTO complaints (student_id, subject, description, status, complaint_date) VALUES (%s, %s, %s, %s, %s)",
        (student["student_id"], data.subject, blank_to_none(data.description),
         data.status or "Submitted", data.date or date.today().isoformat()),
    )
    return {"message": "Complaint submitted"}


@router.put("/{complaint_id}")
def edit_complaint(complaint_id: int, data: ComplaintData):
    # PUT /complaints/2  ->  admin edits it (usually just the status)
    find_or_404("complaints", "complaint_id", complaint_id)
    student = find_student_by_name(data.student)
    change_data(
        "UPDATE complaints SET student_id = %s, subject = %s, description = %s, complaint_date = %s, status = %s WHERE complaint_id = %s",
        (student["student_id"], data.subject, blank_to_none(data.description),
         data.date or date.today().isoformat(), data.status or "Submitted", complaint_id),
    )
    return {"message": "Complaint updated"}


@router.delete("/{complaint_id}")
def delete_complaint(complaint_id: int):
    # DELETE /complaints/2
    find_or_404("complaints", "complaint_id", complaint_id)
    change_data("DELETE FROM complaints WHERE complaint_id = %s", (complaint_id,))
    return {"message": "Complaint deleted"}
