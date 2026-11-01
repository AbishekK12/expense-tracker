# PaisaFlow — Personal Expense Tracker

A full-stack personal finance tracker with a Python/FastAPI backend, JSON-file persistence,
and a React + TypeScript frontend. Currency display is configured to INR (₹).

## Features

- Dashboard with monthly income, expenses, balance, transaction count and recent activity.
- Expense CRUD, search, category/date filters and pagination.
- Income CRUD, search, source/date filters and pagination.
- Category CRUD with expense, income or both types.
- Monthly category budgets with spent, remaining and over-budget calculations.
- Monthly cash-flow analytics and category-wise spending analytics.
- Financial reports with CSV export from the frontend.
- Responsive layout for desktop, tablet and mobile.
- Swagger API documentation at `/docs`.

## Requirements

- Python 3.10+
- Node.js 20+ and npm

## Backend setup (PowerShell)

From the project root:

```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn backend.api.main:app --reload
```

Backend: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/docs

## Frontend setup

Open a second terminal and run:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal (normally http://localhost:5173).

Optional API URL configuration: copy `frontend/.env.example` to `frontend/.env` and
set `VITE_API_BASE_URL` if the API runs somewhere other than `http://127.0.0.1:8000`.

## API overview

| Area | Endpoints |
|---|---|
| Health/config | `GET /api/health`, `GET /api/config` |
| Expenses | `GET/POST /api/expenses`, `GET/PUT/DELETE /api/expenses/{id}` |
| Income | `GET/POST /api/income`, `GET/PUT/DELETE /api/income/{id}` |
| Categories | `GET/POST /api/categories`, `PUT/DELETE /api/categories/{id}` |
| Budgets | `GET/POST /api/budgets`, `PUT/DELETE /api/budgets/{id}` |
| Dashboard | `GET /api/dashboard/summary?month=YYYY-MM` |
| Analytics | `GET /api/analytics/monthly?year=YYYY`, `GET /api/analytics/categories?month=YYYY-MM` |
| Reports | `GET /api/reports?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` |

## Data storage

The app stores records in separate JSON files under `data/`:

- `expenses.json`
- `income.json`
- `categories.json`
- `budgets.json`

Back up this folder regularly. This JSON-backed design is suitable for local learning and
single-user use; it is not a multi-user production database. There is currently no login,
authentication, cloud sync or multi-user isolation.

## Tests

From the project root:

```powershell
python -m pytest -v
```

## Notes

- The INR setting controls display and API metadata. It does not perform foreign-exchange conversion.
- Existing expense fields and JSON storage remain supported. The API assigns UUIDs to legacy expense records on first API access.
- Income is stored separately and does not modify expense records.
- Category names are currently stored as text on transactions; categories provide reusable suggestions and budget grouping.
- Budget spending is calculated from expense category text and the budget month.
