import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent/"expense.json"

def load_expenses() -> list:

    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE,"r",encoding="utf-8") as file:
            expenses = json.load(file)

        if not isinstance(expenses,list):
            raise ValueError("Expenses should be list")
        return expenses 
    except (OSError,ValueError) as e:
        print(f"Error loading student data: {e}")
        return []
    except Exception as e:
        print(f"Error loading student data: {e}")
        return []


def save_expenses(expenses:list) -> None:

    with open(DATA_FILE,"w",encoding="utf-8") as file:
        json.dump(expenses,file,indent=4)