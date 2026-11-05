# Hostel Management - Backend (FastAPI + MariaDB)

A small backend for your hostel project. Plain SQL, no complicated tools.

## How the backend talks to the frontend

Your frontend calls simple addresses like `GET /students` or `DELETE /fees/3`.
Each table has one small file in the `routes/` folder that answers those calls.

The frontend uses field names like `dueDate` and `roomNumber`, but the database
uses `due_date` and `room_number`. The SQL in each route file uses `AS` to
rename columns, so both sides stay happy.

## Setup (do these steps in order)

### 1. Create the database

Make sure MariaDB is running, then open a terminal in THIS folder and run:

    mysql -u root -p < schema.sql

It creates the `hostel_db` database and all 8 tables.

### 2. Install the Python packages

    pip install -r requirements.txt

### 3. Create your .env file

Copy `.env.example` to `.env` (same folder) and fill in your MariaDB password.

### 4. Create the first admin account

    python create_admin.py

It asks for a name, email and password. Remember them - this is your login.

### 5. Start the server

    uvicorn main:app --reload

- API is now at http://127.0.0.1:8000
- Nice test page (Swagger UI): http://127.0.0.1:8000/docs

### 6. Connect the frontend

In `frontend/js/config/config.js` change:

    export const USE_DEMO_DATA = false;

Run the frontend with Live Server (port 5500) so the CORS setting matches.

## Useful things to know

- When you add a student, a LOGIN account is created for them automatically.
  Their password is always `student123` at first.
- In the student form, if you type a room number (like `A-101`), the student is
  moved into that room automatically (if it exists and has a free bed).
- If an admin types a student or room name that does not exist, the backend
  answers with a clear error like: Student "X" not found. Add the student first.
- Login tokens: `POST /login` still works and returns a token. The current
  frontend does not send tokens, so the list pages are open. To lock them,
  add `dependencies=[Depends(admin_only)]` to each APIRouter (see students.py
  comment) AND use the upgraded `api.js` from `optional-frontend-upgrade/`.

## Project layout

    main.py            -> starts the app, connects all the route files
    database.py        -> the only file that opens MariaDB; small helper functions
    auth.py            -> password hashing, tokens, the admin_only guard
    auth_routes.py     -> POST /login
    create_admin.py    -> run once to make the admin account
    schema.sql         -> creates the database (run once)
    routes/
      students.py      -> GET/POST/PUT/DELETE /students
      rooms.py         -> GET/POST/PUT/DELETE /rooms
      allocations.py   -> GET/POST/PUT/DELETE /allocations
      fees.py          -> GET/POST/PUT/DELETE /fees
      complaints.py    -> GET/POST/PUT/DELETE /complaints
      visitors.py      -> GET/POST/PUT/DELETE /visitors
      expenses.py      -> GET/POST/PUT/DELETE /expenses
      reports.py       -> GET /reports/summary (bonus)
      student_portal.py-> GET /student/complaints/{name}, GET /student/fees/{name}
