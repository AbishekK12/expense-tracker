from tracker.expense import Expense

from tracker.validation import validate_name,validate_amount,validate_date,validate_category
from tracker.storage import load_expenses,save_expenses


def add_expense(name:str,amount:float,category:str,date:str) -> dict:

    if not validate_name(name):
        raise ValueError("Expense name cannot be empty")
    if not validate_amount(amount):
        raise ValueError("Expense amount should be greater than zero")
    if not validate_category(category):
        raise ValueError("Category should not be empty")
    if not validate_date(date):
        raise ValueError("Date should be in a given format")

    expenses = load_expenses()


    if expenses:
        next_id = max(expense["expense_id"] for expense in expenses) +1
    else:
        next_id = 1

    expense = Expense(expense_id=next_id,name=name.strip(),amount=float(amount),category=category.strip().upper(),date = date)


    expense_data = expense.to_dict()

    expenses.append(expense_data)

    save_expenses(expenses)

    return expense_data
        