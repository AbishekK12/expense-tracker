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
git clone <>
cd expense_tracker
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
├── expenses.json
├── requirements.txt
├── README.md
├── tracker/
└── tests/
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

*The example values are illustrative.*

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