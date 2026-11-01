from collections import defaultdict
from datetime import date
from fastapi import APIRouter, Query, HTTPException
from backend.api.config import CURRENCY_CODE, CURRENCY_SYMBOL, EXPENSES_FILE, INCOME_FILE
from src.storage import load_expenses
from src.income_storage import load_income

router = APIRouter(tags=["Dashboard & Reports"])

def _records():
    expenses = load_expenses(EXPENSES_FILE)
    incomes = load_income(INCOME_FILE)
    return expenses, incomes

@router.get("/api/dashboard/summary")
def dashboard_summary(month: str | None = None):
    selected = month or date.today().strftime("%Y-%m")
    try:
        date.fromisoformat(selected + "-01")
    except ValueError:
        raise HTTPException(status_code=400, detail="month must use YYYY-MM format.")
    expenses, incomes = _records()
    month_expenses = [e for e in expenses if e.expense_date[:7] == selected]
    month_income = [i for i in incomes if i.income_date[:7] == selected]
    expense_total = round(sum(e.amount for e in month_expenses), 2)
    income_total = round(sum(i.amount for i in month_income), 2)
    all_expenses = round(sum(e.amount for e in expenses), 2)
    all_income = round(sum(i.amount for i in incomes), 2)
    recent = sorted(
        [{"id": e.id, "type": "expense", "description": e.description, "category": e.category, "amount": e.amount, "date": e.expense_date} for e in expenses] +
        [{"id": i.id, "type": "income", "description": i.description, "category": i.source, "amount": i.amount, "date": i.income_date} for i in incomes],
        key=lambda x: x["date"], reverse=True
    )[:8]
    return {
        "month": selected, "currency": CURRENCY_CODE, "currency_symbol": CURRENCY_SYMBOL,
        "income": income_total, "expenses": expense_total, "balance": round(income_total-expense_total, 2),
        "all_time_income": all_income, "all_time_expenses": all_expenses,
        "all_time_balance": round(all_income-all_expenses, 2),
        "transaction_count": len(month_expenses)+len(month_income), "recent_transactions": recent,
    }

@router.get("/api/analytics/monthly")
def monthly_analytics(year: int = Query(default_factory=lambda: date.today().year, ge=2000, le=2100)):
    expenses, incomes = _records()
    rows = {}
    for month in range(1, 13):
        key = f"{year}-{month:02d}"
        rows[key] = {"month": key, "income": 0.0, "expenses": 0.0}
    for e in expenses:
        if e.expense_date.startswith(str(year)+"-"):
            rows[e.expense_date[:7]]["expenses"] += e.amount
    for i in incomes:
        if i.income_date.startswith(str(year)+"-"):
            rows[i.income_date[:7]]["income"] += i.amount
    items = [{**v, "balance": round(v["income"]-v["expenses"], 2)} for v in rows.values()]
    for item in items:
        item["income"] = round(item["income"], 2)
        item["expenses"] = round(item["expenses"], 2)
    return {"year": year, "currency": CURRENCY_CODE, "items": items}

@router.get("/api/analytics/categories")
def category_analytics(month: str | None = None):
    expenses, _ = _records()
    selected = month or date.today().strftime("%Y-%m")
    totals = defaultdict(float)
    for e in expenses:
        if e.expense_date[:7] == selected:
            totals[e.category] += e.amount
    items = [{"category": k, "amount": round(v, 2)} for k, v in sorted(totals.items(), key=lambda x: x[1], reverse=True)]
    return {"month": selected, "currency": CURRENCY_CODE, "items": items}

@router.get("/api/reports")
def financial_report(start_date: date | None = None, end_date: date | None = None):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date cannot be after end_date.")
    expenses, incomes = _records()
    ex = [e for e in expenses if (not start_date or date.fromisoformat(e.expense_date) >= start_date) and (not end_date or date.fromisoformat(e.expense_date) <= end_date)]
    inc = [i for i in incomes if (not start_date or date.fromisoformat(i.income_date) >= start_date) and (not end_date or date.fromisoformat(i.income_date) <= end_date)]
    return {
        "currency": CURRENCY_CODE,
        "start_date": start_date.isoformat() if start_date else None,
        "end_date": end_date.isoformat() if end_date else None,
        "total_income": round(sum(i.amount for i in inc), 2),
        "total_expenses": round(sum(e.amount for e in ex), 2),
        "net_balance": round(sum(i.amount for i in inc)-sum(e.amount for e in ex), 2),
        "income_count": len(inc), "expense_count": len(ex),
        "expenses": [{"description":e.description,"category":e.category,"amount":e.amount,"date":e.expense_date} for e in ex],
        "income": [{"description":i.description,"source":i.source,"amount":i.amount,"date":i.income_date} for i in inc],
    }
