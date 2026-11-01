from datetime import date
from pydantic import BaseModel, ConfigDict, Field, field_validator


class IncomeCreate(BaseModel):
    description: str = Field(min_length=1, max_length=200)
    amount: float = Field(gt=0, allow_inf_nan=False)
    source: str = Field(min_length=1, max_length=80)
    income_date: date

    @field_validator("description", "source")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value


class IncomeUpdate(IncomeCreate):
    pass


class IncomeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    description: str
    amount: float
    source: str
    income_date: date


class IncomeListResponse(BaseModel):
    items: list[IncomeResponse]
    total: int
    currency: str
