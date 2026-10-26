from tracker import calculate_total as calculate_total_module
from tracker.calculate_total import calculate_total


def test_calculate_total(monkeypatch):
    expenses = [
        {"expense_id": 1, "name": "Lunch", "amount": 150.0},
        {"expense_id": 2, "name": "Bus", "amount": 30.0},
        {"expense_id": 3, "name": "Movie", "amount": 250.0},
    ]

    monkeypatch.setattr(
        calculate_total_module,
        "load_expenses",
        lambda: expenses,
    )

    result = calculate_total()

    assert result == 430.0


def test_calculate_total_when_no_expenses(monkeypatch):
    monkeypatch.setattr(
        calculate_total_module,
        "load_expenses",
        lambda: [],
    )

    result = calculate_total()

    assert result == 0.0