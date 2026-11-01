"""Income model and validation."""

from dataclasses import dataclass
from datetime import date
from typing import Any
from uuid import UUID


@dataclass
class Income:
    """Represent one income record."""

    description: str
    amount: float
    source: str
    income_date: str
    id: str | None = None

    def __post_init__(self) -> None:
        self.description = self.description.strip()
        self.source = self.source.strip()
        self.amount = float(self.amount)

        if not self.description:
            raise ValueError("Description cannot be empty.")
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if not self.source:
            raise ValueError("Source cannot be empty.")

        try:
            parsed_date = date.fromisoformat(self.income_date)
        except (TypeError, ValueError) as exc:
            raise ValueError("Date must be in YYYY-MM-DD format.") from exc
        self.income_date = parsed_date.isoformat()

        if self.id is not None:
            try:
                self.id = str(UUID(str(self.id)))
            except (TypeError, ValueError, AttributeError) as exc:
                raise ValueError("Income id must be a valid UUID.") from exc

    def to_dict(self) -> dict[str, Any]:
        data = {
            "description": self.description,
            "amount": self.amount,
            "source": self.source,
            "income_date": self.income_date,
        }
        if self.id is not None:
            data["id"] = self.id
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Income":
        return cls(
            description=str(data["description"]),
            amount=float(data["amount"]),
            source=str(data["source"]),
            income_date=str(data["income_date"]),
            id=str(data["id"]) if data.get("id") is not None else None,
        )
