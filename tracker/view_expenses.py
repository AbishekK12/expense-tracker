from tracker.storage import load_expenses

def view_expenses() -> list:
    expenses = load_expenses()
    return expenses