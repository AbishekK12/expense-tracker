from datetime import date
from pydantic import BaseModel, ConfigDict, Field, field_validator

class ExpenseCreate(BaseModel):
    description: str = Field(min_length=1, max_length=200)
    amount: float = Field(gt=0, allow_inf_nan=False)
    category: str = Field(min_length=1, max_length=80)
    expense_date: date

    @field_validator("description", "category")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value

class ExpenseUpdate(ExpenseCreate):
    pass

class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    description: str
    amount: float
    category: str
    expense_date: date

class ExpenseListResponse(BaseModel):
    items: list[ExpenseResponse]
    total: int
    currency: str
