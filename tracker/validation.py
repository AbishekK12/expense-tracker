from datetime import datetime


def validate_name(name: str) -> bool:
    return bool(name.strip())


def validate_category(category: str) -> bool:
    return bool(category.strip())


def validate_amount(amount: float) -> bool:
    return amount > 0


def validate_amount_input(value: str) -> bool:
    try:
        amount = float(value)
        return amount > 0
    except ValueError:
        return False


def validate_date(date: str) -> bool:
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_valid_input(prompt: str, validator, error_message: str) -> str:
    while True:
        value = input(prompt).strip()

        if validator(value):
            return value

        print(error_message)