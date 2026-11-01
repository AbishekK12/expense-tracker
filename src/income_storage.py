"""JSON persistence for income records."""

import json
from pathlib import Path

from src.income import Income

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INCOME_FILE = PROJECT_ROOT / "data" / "income.json"


def load_income(file_path: str | Path = DEFAULT_INCOME_FILE) -> list[Income]:
    path = Path(file_path)
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Could not read JSON data in {path}: {exc}") from exc

    if not isinstance(raw_data, list):
        raise ValueError("Income JSON must contain a list.")

    records: list[Income] = []
    for index, item in enumerate(raw_data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Income record #{index} must be a JSON object.")
        try:
            records.append(Income.from_dict(item))
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Invalid income record #{index}: {exc}") from exc
    return records


def save_income(records: list[Income], file_path: str | Path = DEFAULT_INCOME_FILE) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump([record.to_dict() for record in records], file, indent=4, ensure_ascii=False)
        file.write("\n")
    temporary_path.replace(path)
