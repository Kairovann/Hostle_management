# Fees owed by students and the payments recorded against them.

from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from database import get_rows, get_row, change_data, find_or_404, find_student_by_name

router = APIRouter(prefix="/fees", tags=["Fees"])

# The frontend wants: id, student, amount, dueDate, status
FEE_SELECT = """
    SELECT f.fee_id AS id, s.student_name AS student, f.amount,
           f.due_date AS dueDate, f.status
    FROM fees f
    JOIN students s ON s.student_id = f.student_id
"""


class FeeData(BaseModel):
    student: Optional[str] = None
    amount: Optional[float] = None
    dueDate: Optional[str] = None
    status: Optional[str] = None   # Pending / Paid / Overdue


def save_fee(student_name, amount, due_date, status, fee_id=None):
    # Shared by add and edit: finds the student, then inserts or updates.
    student = find_student_by_name(student_name)
    payment_date = date.today().isoformat() if status == "Paid" else None

    if fee_id is None:
        change_data(
            "INSERT INTO fees (student_id, amount, due_date, payment_date, status) VALUES (%s, %s, %s, %s, %s)",
            (student["student_id"], amount or 0, due_date, payment_date, status or "Pending"),
        )
    else:
        change_data(
            "UPDATE fees SET student_id = %s, amount = %s, due_date = %s, payment_date = %s, status = %s WHERE fee_id = %s",
            (student["student_id"], amount or 0, due_date, payment_date, status or "Pending", fee_id),
        )


@router.get("")
def list_fees():
    # GET /fees
    return get_rows(FEE_SELECT + " ORDER BY f.fee_id DESC")


@router.post("")
def add_fee(data: FeeData):
    # POST /fees
    save_fee(data.student, data.amount, data.dueDate, data.status)
    return {"message": "Fee added"}


@router.put("/{fee_id}")
def edit_fee(fee_id: int, data: FeeData):
    # PUT /fees/4
    find_or_404("fees", "fee_id", fee_id)
    save_fee(data.student, data.amount, data.dueDate, data.status, fee_id)
    return {"message": "Fee updated"}


@router.delete("/{fee_id}")
def delete_fee(fee_id: int):
    # DELETE /fees/4
    find_or_404("fees", "fee_id", fee_id)
    change_data("DELETE FROM fees WHERE fee_id = %s", (fee_id,))
    return {"message": "Fee deleted"}
