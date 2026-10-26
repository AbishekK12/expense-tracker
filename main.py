from tracker.validation import validate_date,validate_amount_input,validate_name,validate_category,get_valid_input
from tracker.add_expense import add_expense
from tracker.delete_expense import delete_expense
from tracker.view_expenses import view_expenses
from tracker.calculate_total import calculate_total
from tracker.category_sum import category_sum


def menu():

    print("\n-------------------Expense Tracker---------------------------")
    print("1. Add Expense\n2. View Expenses\n3. Delete Expenses\n4. Calculate Total Expenses\n5. Category Summary\n6. Exit")


def handle_add_expense():
    try:
        name = get_valid_input(
            prompt="Enter expense name: ",
            validator=validate_name,
            error_message="Expense name cannot be empty.",
        )

        amount = get_valid_input(
            prompt="Enter amount: ",
            validator=validate_amount_input,
            error_message="Enter a valid positive amount.",
        )

        category = get_valid_input(
            prompt="Enter category: ",
            validator=validate_category,
            error_message="Category cannot be empty.",
        )

        date = get_valid_input(
            prompt="Enter date (YYYY-MM-DD): ",
            validator=validate_date,
            error_message="Enter a valid date in YYYY-MM-DD format.",
        )

        expense = add_expense(
            name=name,
            amount=float(amount),
            category=category,
            date=date,
        )

        print("\nExpense added successfully!")
        print(f"Expense ID: {expense['expense_id']}")
        print(f"Name: {expense['name']}")
        print(f"Amount: ₹{expense['amount']:.2f}")
        print(f"Category: {expense['category']}")
        print(f"Date: {expense['date']}")

    except ValueError as error:
        print(f"\nUnable to add expense: {error}")

def handle_view_expenses():

    expenses = view_expenses()

    if not expenses:
        print("\n No expenses is found")
        return

    print("-----My expenses -----")

    for expense in expenses:
        print(
            f"Id: {expense['expense_id']} | "
            f"Name: {expense['name']} | "
            f"Amount: {expense['amount']} | "
            f"Category: {expense['category']} | "
            f"Date: {expense['date']}"
        )

def handle_delete_expense():

    try:

        expense_id = int(input("Enter the id to delete: "))

        deleted = delete_expense(expense_id)

        if deleted:
            print("Deleted Successfully")
        else:
            print("Expense ID not found")
    except ValueError as error:
        print("Please enter the valid numberic number" , error)



def handle_calculate_total():
    total = calculate_total()
    print("Total Amount Spended is " , total)


def handle_category_summary():

    summary = category_sum()

    if not summary:
        print("Expenses is unavailable")
        return

    print("------Category based Total---------")

    for category, amount in summary.items():
        print(f"{category} : ${amount:.2f}")



def main():

    while True:

        menu()

        choice = input("Enter the choice : ").strip()

        if choice == "1":
            handle_add_expense()
        elif choice == "2":
            handle_view_expenses()
        elif choice == "3":
            handle_delete_expense()
        elif choice == "4":
            handle_calculate_total()
        elif choice == "5":
            handle_category_summary()
        elif choice == "6":
            print("Thanks!.....")
            break
        else:
            print("Enter the choice between 1-6 ")


if __name__ == "__main__":
    main()
        
