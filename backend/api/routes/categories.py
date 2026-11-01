from uuid import uuid4
from fastapi import APIRouter, HTTPException, Response, status
from backend.api.config import CATEGORIES_FILE
from backend.api.schemas.category import CategoryCreate, CategoryUpdate
from src.json_store import load_records, save_records

router = APIRouter(prefix="/api/categories", tags=["Categories"])

@router.get("")
def list_categories(kind: str | None = None):
    records = load_records(CATEGORIES_FILE)
    if kind:
        records = [r for r in records if r.get("kind") in (kind, "both")]
    return {"items": records, "total": len(records)}

@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate):
    records = load_records(CATEGORIES_FILE)
    if any(r["name"].casefold() == payload.name.casefold() and r["kind"] == payload.kind for r in records):
        raise HTTPException(status_code=409, detail="A category with this name and type already exists.")
    item = {"id": str(uuid4()), **payload.model_dump()}
    records.append(item)
    save_records(records, CATEGORIES_FILE)
    return item

@router.put("/{category_id}")
def update_category(category_id: str, payload: CategoryUpdate):
    records = load_records(CATEGORIES_FILE)
    for i, current in enumerate(records):
        if current["id"] == category_id:
            if any(r["id"] != category_id and r["name"].casefold() == payload.name.casefold() and r["kind"] == payload.kind for r in records):
                raise HTTPException(status_code=409, detail="A category with this name and type already exists.")
            updated = {"id": category_id, **payload.model_dump()}
            records[i] = updated
            save_records(records, CATEGORIES_FILE)
            return updated
    raise HTTPException(status_code=404, detail="Category not found.")

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str):
    records = load_records(CATEGORIES_FILE)
    remaining = [r for r in records if r["id"] != category_id]
    if len(remaining) == len(records):
        raise HTTPException(status_code=404, detail="Category not found.")
    save_records(remaining, CATEGORIES_FILE)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
