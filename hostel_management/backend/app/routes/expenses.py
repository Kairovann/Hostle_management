# Everything about hostel expenses (bills, repairs, etc.)
#
# Frontend field  ->  Database column
#   title         ->  expense_name
#   date          ->  expense_date
#   notes         ->  description

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from database import get_rows, get_row, change_data, find_or_404, blank_to_none

router = APIRouter(prefix="/expenses", tags=["Expenses"])

EXPENSE_SELECT = """
    SELECT e.expense_id AS id, e.expense_name AS title, e.category,
           e.amount, e.expense_date AS date, e.description AS notes
    FROM expenses e
"""


class ExpenseData(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[str] = None
    notes: Optional[str] = None


@router.get("")
def list_expenses():
    # GET /expenses
    return get_rows(EXPENSE_SELECT + " ORDER BY e.expense_date DESC, e.expense_id DESC")


@router.post("")
def add_expense(data: ExpenseData):
    # POST /expenses
    change_data(
        "INSERT INTO expenses (expense_name, category, amount, expense_date, description) VALUES (%s, %s, %s, %s, %s)",
        (data.title, blank_to_none(data.category), data.amount or 0,
         data.date, blank_to_none(data.notes)),
    )
    return {"message": "Expense added"}


@router.put("/{expense_id}")
def edit_expense(expense_id: int, data: ExpenseData):
    # PUT /expenses/5
    find_or_404("expenses", "expense_id", expense_id)
    change_data(
        "UPDATE expenses SET expense_name = %s, category = %s, amount = %s, expense_date = %s, description = %s WHERE expense_id = %s",
        (data.title, blank_to_none(data.category), data.amount or 0,
         data.date, blank_to_none(data.notes), expense_id),
    )
    return {"message": "Expense updated"}


@router.delete("/{expense_id}")
def delete_expense(expense_id: int):
    # DELETE /expenses/5
    find_or_404("expenses", "expense_id", expense_id)
    change_data("DELETE FROM expenses WHERE expense_id = %s", (expense_id,))
    return {"message": "Expense deleted"}
