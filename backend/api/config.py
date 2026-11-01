from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
EXPENSES_FILE = DATA_DIR / "expenses.json"
INCOME_FILE = DATA_DIR / "income.json"
CATEGORIES_FILE = DATA_DIR / "categories.json"
BUDGETS_FILE = DATA_DIR / "budgets.json"
CURRENCY_CODE = "INR"
CURRENCY_SYMBOL = "₹"
