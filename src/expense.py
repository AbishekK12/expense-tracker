"""Expense model and validation."""

from dataclasses import dataclass
from datetime import date
from typing import Any
from uuid import UUID


@dataclass
class Expense:
    """Represent one expense."""

    description: str
    amount: float
    category: str
    expense_date: str
    id: str | None = None

    def __post_init__(self) -> None:
        self.description = self.description.strip()
        self.category = self.category.strip()
        self.amount = float(self.amount)

        if not self.description:
            raise ValueError("Description cannot be empty.")
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if not self.category:
            raise ValueError("Category cannot be empty.")

        try:
            parsed_date = date.fromisoformat(self.expense_date)
        except (TypeError, ValueError) as exc:
            raise ValueError("Date must be in YYYY-MM-DD format.") from exc
        self.expense_date = parsed_date.isoformat()
        if self.id is not None:
            try:
                self.id = str(UUID(str(self.id)))
            except (TypeError, ValueError, AttributeError) as exc:
                raise ValueError("Expense id must be a valid UUID.") from exc

    def to_dict(self) -> dict[str, Any]:
        """Convert the expense to a JSON-compatible dictionary."""
        data = {
            "description": self.description,
            "amount": self.amount,
            "category": self.category,
            "expense_date": self.expense_date,
        }
        # Keep the original four-field format for legacy/CLI-created records.
        if self.id is not None:
            data["id"] = self.id
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Expense":
        """Create an Expense from a dictionary."""
        return cls(
            description=str(data["description"]),
            amount=float(data["amount"]),
            category=str(data["category"]),
            expense_date=str(data["expense_date"]),
            id=str(data["id"]) if data.get("id") is not None else None,
        )
