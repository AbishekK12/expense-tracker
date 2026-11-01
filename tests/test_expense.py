"""Tests for Expense model and JSON storage."""

import json

import pytest

from src.expense import Expense
from src.storage import load_expenses, save_expenses


def make_expense(
    description: str = "Lunch",
    amount: float = 12.5,
    category: str = "Food",
    expense_date: str = "2026-10-20",
) -> Expense:
    return Expense(description, amount, category, expense_date)


def test_expense_to_dict_contains_expected_fields() -> None:
    expense = make_expense()
    assert expense.to_dict() == {
        "description": "Lunch",
        "amount": 12.5,
        "category": "Food",
        "expense_date": "2026-10-20",
    }


def test_expense_rejects_non_positive_amount() -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        make_expense(amount=0)


def test_expense_rejects_invalid_date() -> None:
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        make_expense(expense_date="20-10-2026")


def test_save_and_load_expenses_round_trip(tmp_path) -> None:
    path = tmp_path / "data" / "expenses.json"
    original = [make_expense(), make_expense("Bus", 3.0, "Travel")]
    save_expenses(original, path)
    loaded = load_expenses(path)
    assert [item.to_dict() for item in loaded] == [
        item.to_dict() for item in original
    ]


def test_missing_json_file_returns_empty_list(tmp_path) -> None:
    assert load_expenses(tmp_path / "missing.json") == []


def test_malformed_json_raises_clear_error(tmp_path) -> None:
    path = tmp_path / "expenses.json"
    path.write_text("{invalid json", encoding="utf-8")
    with pytest.raises(ValueError, match="Could not read JSON"):
        load_expenses(path)
