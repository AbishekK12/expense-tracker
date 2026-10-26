from tracker.expense import Expense


def test_expense_creation():
    expense = Expense(
        1,
        "Lunch",
        150.0,
        "Food",
        "2026-10-26"
    )

    assert expense.name == "Lunch"
    assert expense.amount == 150.0
    assert expense.category == "Food"


def test_expense_to_dict():
    expense = Expense(
        1,
        "Lunch",
        150.0,
        "Food",
        "2026-10-26"
    )

    result = expense.to_dict()

    assert result["expense_id"] == 1
    assert result["name"] == "Lunch"
    assert result["amount"] == 150.0