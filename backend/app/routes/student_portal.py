# Endpoints for the STUDENT side of the app.
# The current frontend reads everything through the normal lists instead,
# so these are bonus endpoints you can try in the docs page:
#   http://127.0.0.1:8000/docs

from fastapi import APIRouter

from database import get_rows

router = APIRouter(prefix="/student", tags=["Student Portal"])


@router.get("/complaints/{student_name}")
def my_complaints(student_name: str):
    # GET /student/complaints/Aarav Sharma  ->  that student's complaints
    return get_rows(
        """SELECT c.complaint_id AS id, c.subject, c.description,
                  DATE(c.complaint_date) AS date, c.status
           FROM complaints c
           JOIN students s ON s.student_id = c.student_id
           WHERE s.student_name = %s
           ORDER BY c.complaint_id DESC""",
        (student_name,),
    )


@router.get("/fees/{student_name}")
def my_fees(student_name: str):
    # GET /student/fees/Aarav Sharma  ->  that student's fees
    return get_rows(
        """SELECT f.fee_id AS id, f.amount, f.due_date AS dueDate,
                  f.payment_date AS paymentDate, f.status
           FROM fees f
           JOIN students s ON s.student_id = f.student_id
           WHERE s.student_name = %s
           ORDER BY f.fee_id DESC""",
        (student_name,),
    )
