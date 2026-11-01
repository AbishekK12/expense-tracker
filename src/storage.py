"""JSON persistence for expenses."""

import json
from pathlib import Path

from src.expense import Expense

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_FILE = PROJECT_ROOT / "data" / "expenses.json"


def load_expenses(file_path: str | Path = DEFAULT_DATA_FILE) -> list[Expense]:
    """Load expenses from JSON; return an empty list if the file does not exist."""
    path = Path(file_path)
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Could not read JSON data in {path}: {exc}") from exc

    if not isinstance(raw_data, list):
        raise ValueError("Expenses JSON must contain a list.")

    expenses = []
    for index, item in enumerate(raw_data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Expense record #{index} must be a JSON object.")
        try:
            expenses.append(Expense.from_dict(item))
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Invalid expense record #{index}: {exc}") from exc
    return expenses


def save_expenses(
    expenses: list[Expense], file_path: str | Path = DEFAULT_DATA_FILE
) -> None:
    """Save expenses to JSON, creating the parent folder if needed."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(
            [expense.to_dict() for expense in expenses],
            file,
            indent=4,
            ensure_ascii=False,
        )
        file.write("\n")
    temporary_path.replace(path)
