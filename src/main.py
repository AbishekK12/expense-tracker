"""Command-line entry point for the Expense Tracker."""

from pathlib import Path

from src.expense import Expense
from src.storage import DEFAULT_DATA_FILE, load_expenses, save_expenses
from src.utils import prompt_non_empty, today_iso


def display_expenses(expenses: list[Expense]) -> None:
    """Print all saved expenses."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print("\n--- All Expenses ---")
    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index}. {expense.expense_date} | {expense.category} | "
            f"{expense.description} | {expense.amount:.2f}"
        )


def display_category_totals(expenses: list[Expense]) -> None:
    """Print total spending grouped by category."""
    totals: dict[str, float] = {}
    for expense in expenses:
        totals[expense.category] = totals.get(expense.category, 0.0) + expense.amount

    if not totals:
        print("\nNo expenses available to total.")
        return

    print("\n--- Totals by Category ---")
    for category, total in sorted(totals.items(), key=lambda item: item[0].lower()):
        print(f"{category}: {total:.2f}")


def add_expense(expenses: list[Expense]) -> None:
    """Collect, validate, and append one expense."""
    print("\n--- Add Expense ---")
    description = prompt_non_empty("Description: ")
    category = prompt_non_empty("Category (e.g. Food, Travel): ")

    while True:
        try:
            amount = float(input("Amount: ").strip())
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            break
        except ValueError as exc:
            print(f"Invalid amount: {exc}. Please enter a positive number.")

    while True:
        expense_date = input(f"Date YYYY-MM-DD [{today_iso()}]: ").strip()
        if not expense_date:
            expense_date = today_iso()
        try:
            expense = Expense(description, amount, category, expense_date)
            break
        except ValueError as exc:
            print(f"Invalid expense: {exc}")

    expenses.append(expense)
    save_expenses(expenses)
    print("Expense saved successfully.")


def print_menu() -> None:
    print("\n========== Expense Tracker ==========")
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Show totals by category")
    print("4. Exit")


def main() -> None:
    """Run the application menu."""
    try:
        expenses = load_expenses()
    except (OSError, ValueError) as exc:
        print(f"Could not load saved expenses: {exc}")
        print(f"Check the data file: {DEFAULT_DATA_FILE}")
        expenses = []

    while True:
        print_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            try:
                add_expense(expenses)
            except OSError as exc:
                print(f"Could not save expense: {exc}")
        elif choice == "2":
            display_expenses(expenses)
        elif choice == "3":
            display_category_totals(expenses)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
