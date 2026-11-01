from pydantic import BaseModel, Field, field_validator
from typing import Literal

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    kind: Literal["expense", "income", "both"] = "expense"
    color: str = Field(default="#64748b", pattern=r"^#[0-9A-Fa-f]{6}$")

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Category name cannot be empty.")
        return value

class CategoryUpdate(CategoryCreate):
    pass
