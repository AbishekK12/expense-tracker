from tracker.storage import load_expenses


def calculate_total() -> float:
    expenses = load_expenses()

    total = 0.0

    for expense in expenses:
        total += expense["amount"]

    return total