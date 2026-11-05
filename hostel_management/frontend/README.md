# HostelDesk — Frontend

A beginner-friendly hostel management frontend built with HTML, CSS and vanilla JavaScript.

## 1. Run the project

Open a terminal in this folder and run:

```bash
python3 -m http.server 5500
```

Then open:

`http://localhost:5500`

Do not open `index.html` directly with `file://`. JavaScript modules need a local web server.

## 2. Demo login accounts

| Role | Email | Password |
|---|---|---|
| Admin | admin@hostel.com | admin123 |
| Student | student@hostel.com | student123 |

## 3. What works in demo mode

- Admin and student login screens
- Separate admin and student dashboards
- Student, room, allocation, fee, complaint, visitor and expense records
- Add, edit, delete and search records
- Student complaint submission and complaint status display
- Reports and print layout
- Data persists in browser `localStorage`

## 4. Backend integration later

The frontend currently uses demo data in `js/services/api.js`.

In `js/config/config.js`:

- Set `USE_DEMO_DATA` to `false` when your FastAPI endpoints are ready.
- Set `API_BASE_URL` to your FastAPI server URL.

Then update the endpoint paths and request/response field names in the service layer to match your FastAPI routes.

**Important:** The current login is only a frontend demonstration. Do not use it as real authentication. Real password verification, sessions or tokens, role permissions, validation and database operations must be implemented in FastAPI. Never store real passwords in frontend JavaScript or `localStorage`.

## 5. Folder layout

- `css/` — global styles and page styles
- `js/components/` — reusable interface components
- `js/config/` — frontend configuration
- `js/logic/` — small validation and page helper functions
- `js/pages/` — page-specific JavaScript
- `js/services/` — API and data access layer
- `pages/` — HTML pages for admin and student roles
