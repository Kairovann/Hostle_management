# Start the server with:   uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import auth_routes
from routes import (
    students,
    rooms,
    allocations,
    fees,
    complaints,
    visitors,
    expenses,
    reports,
    student_portal,
)

app = FastAPI(title="Hostel Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(students.router)
app.include_router(rooms.router)
app.include_router(allocations.router)
app.include_router(fees.router)
app.include_router(complaints.router)
app.include_router(visitors.router)
app.include_router(expenses.router)
app.include_router(reports.router)
app.include_router(student_portal.router)


@app.get("/")
def home():
    return {"message": "Hostel API is running"}

