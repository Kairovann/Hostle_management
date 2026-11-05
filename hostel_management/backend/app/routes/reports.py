# A small summary used by the Reports page.
# The current frontend calculates reports itself from the other lists,
# so it does not call this - but it is here if you want it later.

from fastapi import APIRouter

from database import get_row

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/summary")
def summary():
    # GET /reports/summary  ->  one JSON object with all the headline numbers
    students = get_row("SELECT COUNT(*) AS n FROM students")["n"]
    rooms = get_row("SELECT COUNT(*) AS n FROM rooms")["n"]
    occupied = get_row("SELECT COUNT(*) AS n FROM room_allocations WHERE checkout_date IS NULL")["n"]
    beds = get_row("SELECT COALESCE(SUM(capacity), 0) AS n FROM rooms")["n"]
    collected = get_row("SELECT COALESCE(SUM(amount), 0) AS n FROM fees WHERE status = 'Paid'")["n"]
    pending = get_row("SELECT COALESCE(SUM(amount), 0) AS n FROM fees WHERE status != 'Paid'")["n"]
    expenses = get_row("SELECT COALESCE(SUM(amount), 0) AS n FROM expenses")["n"]
    open_complaints = get_row("SELECT COUNT(*) AS n FROM complaints WHERE status != 'Resolved'")["n"]

    return {
        "students": students,
        "rooms": rooms,
        "occupied_beds": occupied,
        "total_beds": beds,
        "fees_collected": collected,
        "fees_pending": pending,
        "total_expenses": expenses,
        "open_complaints": open_complaints,
    }
