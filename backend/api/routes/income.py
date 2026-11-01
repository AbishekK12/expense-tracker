from datetime import date
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query, Response, status

from src.income import Income
from src.income_storage import load_income, save_income
from backend.api.config import CURRENCY_CODE, INCOME_FILE
from backend.api.schemas.income import (
    IncomeCreate, IncomeListResponse, IncomeResponse, IncomeUpdate,
)

router = APIRouter(prefix="/api/income", tags=["Income"])


def _load_with_ids() -> list[Income]:
    records = load_income(INCOME_FILE)
    changed = False
    for record in records:
        if record.id is None:
            record.id = str(uuid4())
            changed = True
    if changed:
        save_income(records, INCOME_FILE)
    return records


def _to_response(record: Income) -> IncomeResponse:
    return IncomeResponse(
        id=record.id,
        description=record.description,
        amount=record.amount,
        source=record.source,
        income_date=date.fromisoformat(record.income_date),
    )


@router.get("", response_model=IncomeListResponse)
def list_income(
    search: str | None = Query(default=None, max_length=100),
    source: str | None = Query(default=None, max_length=80),
    start_date: date | None = None,
    end_date: date | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date cannot be after end_date.")

    records = _load_with_ids()
    filtered = records
    if search:
        term = search.casefold()
        filtered = [
            item for item in filtered
            if term in item.description.casefold() or term in item.source.casefold()
        ]
    if source:
        filtered = [item for item in filtered if item.source.casefold() == source.casefold()]
    if start_date:
        filtered = [item for item in filtered if date.fromisoformat(item.income_date) >= start_date]
    if end_date:
        filtered = [item for item in filtered if date.fromisoformat(item.income_date) <= end_date]

    filtered.sort(key=lambda item: (item.income_date, item.id or ""), reverse=True)
    total = len(filtered)
    return IncomeListResponse(
        items=[_to_response(item) for item in filtered[skip:skip + limit]],
        total=total,
        currency=CURRENCY_CODE,
    )


@router.post("", response_model=IncomeResponse, status_code=status.HTTP_201_CREATED)
def create_income(payload: IncomeCreate):
    records = _load_with_ids()
    record = Income(
        description=payload.description,
        amount=payload.amount,
        source=payload.source,
        income_date=payload.income_date.isoformat(),
        id=str(uuid4()),
    )
    records.append(record)
    save_income(records, INCOME_FILE)
    return _to_response(record)


@router.get("/{income_id}", response_model=IncomeResponse)
def get_income(income_id: str):
    record = next((item for item in _load_with_ids() if item.id == income_id), None)
    if record is None:
        raise HTTPException(status_code=404, detail="Income record not found.")
    return _to_response(record)


@router.put("/{income_id}", response_model=IncomeResponse)
def update_income(income_id: str, payload: IncomeUpdate):
    records = _load_with_ids()
    for index, current in enumerate(records):
        if current.id == income_id:
            updated = Income(
                description=payload.description,
                amount=payload.amount,
                source=payload.source,
                income_date=payload.income_date.isoformat(),
                id=income_id,
            )
            records[index] = updated
            save_income(records, INCOME_FILE)
            return _to_response(updated)
    raise HTTPException(status_code=404, detail="Income record not found.")


@router.delete("/{income_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_income(income_id: str):
    records = _load_with_ids()
    remaining = [item for item in records if item.id != income_id]
    if len(remaining) == len(records):
        raise HTTPException(status_code=404, detail="Income record not found.")
    save_income(remaining, INCOME_FILE)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
