from pydantic import BaseModel, Field, field_validator
import re

class BudgetCreate(BaseModel):
    category: str = Field(min_length=1, max_length=80)
    month: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")
    amount: float = Field(gt=0, allow_inf_nan=False)

    @field_validator("category")
    @classmethod
    def clean_category(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Category cannot be empty.")
        return value

class BudgetUpdate(BudgetCreate):
    pass
