from datetime import date
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query, Response, status

from src.expense import Expense
from src.storage import load_expenses, save_expenses
from backend.api.config import CURRENCY_CODE, EXPENSES_FILE
from backend.api.schemas.expense import (
    ExpenseCreate, ExpenseListResponse, ExpenseResponse, ExpenseUpdate
)

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])

def _load_with_ids() -> list[Expense]:
    expenses = load_expenses(EXPENSES_FILE)
    changed = False
    for expense in expenses:
        if expense.id is None:
            expense.id = str(uuid4())
            changed = True
    if changed:
        save_expenses(expenses, EXPENSES_FILE)
    return expenses

def _to_response(expense: Expense) -> ExpenseResponse:
    return ExpenseResponse(
        id=expense.id,
        description=expense.description,
        amount=expense.amount,
        category=expense.category,
        expense_date=date.fromisoformat(expense.expense_date),
    )

@router.get("", response_model=ExpenseListResponse)
def list_expenses(
    search: str | None = Query(default=None, max_length=100),
    category: str | None = Query(default=None, max_length=80),
    start_date: date | None = None,
    end_date: date | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date cannot be after end_date.")
    expenses = _load_with_ids()
    filtered = expenses
    if search:
        term = search.casefold()
        filtered = [e for e in filtered if term in e.description.casefold() or term in e.category.casefold()]
    if category:
        filtered = [e for e in filtered if e.category.casefold() == category.casefold()]
    if start_date:
        filtered = [e for e in filtered if date.fromisoformat(e.expense_date) >= start_date]
    if end_date:
        filtered = [e for e in filtered if date.fromisoformat(e.expense_date) <= end_date]
    filtered.sort(key=lambda e: (e.expense_date, e.id or ""), reverse=True)
    total = len(filtered)
    return ExpenseListResponse(
        items=[_to_response(e) for e in filtered[skip:skip + limit]],
        total=total,
        currency=CURRENCY_CODE,
    )

@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(payload: ExpenseCreate):
    expenses = _load_with_ids()
    expense = Expense(
        description=payload.description,
        amount=payload.amount,
        category=payload.category,
        expense_date=payload.expense_date.isoformat(),
        id=str(uuid4()),
    )
    expenses.append(expense)
    save_expenses(expenses, EXPENSES_FILE)
    return _to_response(expense)

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: str):
    expense = next((e for e in _load_with_ids() if e.id == expense_id), None)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found.")
    return _to_response(expense)

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: str, payload: ExpenseUpdate):
    expenses = _load_with_ids()
    for index, current in enumerate(expenses):
        if current.id == expense_id:
            updated = Expense(
                description=payload.description,
                amount=payload.amount,
                category=payload.category,
                expense_date=payload.expense_date.isoformat(),
                id=expense_id,
            )
            expenses[index] = updated
            save_expenses(expenses, EXPENSES_FILE)
            return _to_response(updated)
    raise HTTPException(status_code=404, detail="Expense not found.")

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: str):
    expenses = _load_with_ids()
    remaining = [e for e in expenses if e.id != expense_id]
    if len(remaining) == len(expenses):
        raise HTTPException(status_code=404, detail="Expense not found.")
    save_expenses(remaining, EXPENSES_FILE)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
