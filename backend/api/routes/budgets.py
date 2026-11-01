from uuid import uuid4
from fastapi import APIRouter, HTTPException, Response, status
from backend.api.config import BUDGETS_FILE, EXPENSES_FILE, CURRENCY_CODE
from backend.api.schemas.budget import BudgetCreate, BudgetUpdate
from src.json_store import load_records, save_records
from src.storage import load_expenses

router = APIRouter(prefix="/api/budgets", tags=["Budgets"])

def _budget_view(record: dict):
    expenses = load_expenses(EXPENSES_FILE)
    spent = sum(e.amount for e in expenses if e.category.casefold() == record["category"].casefold() and e.expense_date[:7] == record["month"])
    amount = float(record["amount"])
    return {**record, "amount": amount, "spent": round(spent, 2), "remaining": round(max(amount-spent, 0), 2), "over_budget": spent > amount, "currency": CURRENCY_CODE}

@router.get("")
def list_budgets(month: str | None = None):
    records = load_records(BUDGETS_FILE)
    if month:
        records = [r for r in records if r["month"] == month]
    items = [_budget_view(r) for r in records]
    return {"items": items, "total": len(items)}

@router.post("", status_code=status.HTTP_201_CREATED)
def create_budget(payload: BudgetCreate):
    records = load_records(BUDGETS_FILE)
    if any(r["category"].casefold() == payload.category.casefold() and r["month"] == payload.month for r in records):
        raise HTTPException(status_code=409, detail="A budget already exists for this category and month.")
    item = {"id": str(uuid4()), **payload.model_dump()}
    records.append(item)
    save_records(records, BUDGETS_FILE)
    return _budget_view(item)

@router.put("/{budget_id}")
def update_budget(budget_id: str, payload: BudgetUpdate):
    records = load_records(BUDGETS_FILE)
    for i, current in enumerate(records):
        if current["id"] == budget_id:
            if any(r["id"] != budget_id and r["category"].casefold() == payload.category.casefold() and r["month"] == payload.month for r in records):
                raise HTTPException(status_code=409, detail="A budget already exists for this category and month.")
            updated = {"id": budget_id, **payload.model_dump()}
            records[i] = updated
            save_records(records, BUDGETS_FILE)
            return _budget_view(updated)
    raise HTTPException(status_code=404, detail="Budget not found.")

@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(budget_id: str):
    records = load_records(BUDGETS_FILE)
    remaining = [r for r in records if r["id"] != budget_id]
    if len(remaining) == len(records):
        raise HTTPException(status_code=404, detail="Budget not found.")
    save_records(remaining, BUDGETS_FILE)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
