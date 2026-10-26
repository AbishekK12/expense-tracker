# 💰 Expense Tracker

A beginner-friendly command-line application built with Python to manage daily expenses and track spending by category.

## ✨ Features

- ➕ Add expenses
- 📋 View all expenses
- 🗑️ Delete expenses
- 💵 Calculate total spending
- 📊 View spending by category
- 💾 Store expenses in a JSON file
- ✅ Validate user input
- 🧪 Automated testing with Pytest

## 🛠️ Requirements

- Python 3.10 or newer
- pip

## 🚀 How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/AbishekK12/expense-tracker.git
cd expense-tracker
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start the Application

```bash
python main.py
```

Follow the menu displayed in the terminal to manage your expenses.

## 🧪 Run Tests

Run the following command from the project root:

```bash
python -m pytest -v
```

## 📂 Project Structure

```text
expense_tracker/
├── main.py
├── expense.json
├── requirements.txt
├── README.md
├── tracker/
│   ├── __init__.py
│   ├── expense.py
│   ├── validation.py
│   ├── storage.py
│   ├── add_expense.py
│   ├── view_expenses.py
│   ├── delete_expense.py
│   ├── calculate_total.py
│   └── category_sum.py
└── tests/
    ├── test_expense.py
    ├── test_validation.py
    ├── test_storage.py
    ├── test_add_expense.py
    ├── test_view_expenses.py
    ├── test_delete_expense.py
    ├── test_calculate_total.py
    └── test_category_summary.py
```

## 💻 Example Output

```text
========== EXPENSE TRACKER ==========

1. Add Expense
2. View All Expenses
3. Delete Expense
4. Calculate Total Expenses
5. Show Totals by Category
6. Exit

Choose an option (1-6): 5

========== CATEGORY SUMMARY ==========

Food: ₹450.00
Travel: ₹120.00
Entertainment: ₹300.00

Total Spending: ₹870.00
```

*Note: The example values are illustrative. Actual results depend on the expenses you enter.*

## ✅ Program Checklist

- [x] Create an `Expense` class.
- [x] Add new expenses.
- [x] View all saved expenses.
- [x] Delete expenses by ID.
- [x] Calculate total expenses.
- [x] Display totals by category.
- [x] Save and load expenses using JSON.
- [x] Validate user input.
- [x] Handle invalid input using exceptions.
- [x] Write automated tests using Pytest.
- [x] Create a README with setup and run instructions.
- [x] Upload the project to GitHub.

## 🎯 Concepts Practiced

- Python classes and objects
- Functions and modules
- JSON file handling
- Input validation
- Exception handling
- Automated testing with Pytest
- Git and GitHub

---

⭐ Built with Python as a hands-on learning project.
