from tracker.storage import load_expenses,save_expenses


def delete_expense(expense_id:int) -> bool:

    expenses = load_expenses()

    for expense in expenses:
        if expense["expense_id"] == expense_id:
            expenses.remove(expense)
            save_expenses(expenses)
            return True
    return False