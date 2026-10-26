from tracker.storage import load_expenses


def category_sum() -> dict:
    expenses = load_expenses()

    summary = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        if category in summary:
            summary[category] += amount
        else:
            summary[category] = amount

    return summary