from tracker import category_sum as category_summary_module
from tracker.category_sum import category_sum


def test_category_summary(monkeypatch):
    expenses = [
        {
            "expense_id": 1,
            "name": "Lunch",
            "amount": 150.0,
            "category": "Food",
            "date": "2026-10-26",
        },
        {
            "expense_id": 2,
            "name": "Bus",
            "amount": 30.0,
            "category": "Travel",
            "date": "2026-10-26",
        },
        {
            "expense_id": 3,
            "name": "Dinner",
            "amount": 250.0,
            "category": "Food",
            "date": "2026-10-26",
        },
    ]

    monkeypatch.setattr(
        category_summary_module,
        "load_expenses",
        lambda: expenses,
    )

    result = category_sum()

    assert result == {
        "Food": 400.0,
        "Travel": 30.0,
    }


def test_category_summary_when_no_expenses(monkeypatch):
    monkeypatch.setattr(
        category_summary_module,
        "load_expenses",
        lambda: [],
    )

    result = category_sum()

    assert result == {}