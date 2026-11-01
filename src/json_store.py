"""Small atomic JSON-list persistence helper for additional resources."""
import json
from pathlib import Path
from typing import Any

def load_records(path: str | Path) -> list[dict[str, Any]]:
    target = Path(path)
    if not target.exists():
        return []
    try:
        with target.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Could not read JSON data in {target}: {exc}") from exc
    if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
        raise ValueError(f"{target.name} must contain a JSON list of objects.")
    return data

def save_records(records: list[dict[str, Any]], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)
        file.write("\n")
    temporary.replace(target)
