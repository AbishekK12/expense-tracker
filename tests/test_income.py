import pytest

from src.income import Income
from src.income_storage import load_income, save_income


def make_income(description="Salary", amount=25000, source="Job", income_date="2026-11-01"):
    return Income(description, amount, source, income_date)


def test_income_to_dict_contains_expected_fields():
    record = make_income()
    assert record.to_dict() == {
        "description": "Salary",
        "amount": 25000.0,
        "source": "Job",
        "income_date": "2026-11-01",
    }


def test_income_rejects_non_positive_amount():
    with pytest.raises(ValueError, match="greater than zero"):
        make_income(amount=0)


def test_income_rejects_empty_source():
    with pytest.raises(ValueError, match="Source cannot be empty"):
        make_income(source="   ")


def test_income_rejects_invalid_date():
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        make_income(income_date="01-11-2026")


def test_income_storage_round_trip(tmp_path):
    path = tmp_path / "data" / "income.json"
    original = [make_income(), make_income("Freelance", 5000, "Client")]
    save_income(original, path)
    loaded = load_income(path)
    assert [item.to_dict() for item in loaded] == [item.to_dict() for item in original]


def test_missing_income_file_returns_empty_list(tmp_path):
    assert load_income(tmp_path / "missing.json") == []


def test_malformed_income_json_raises_clear_error(tmp_path):
    path = tmp_path / "income.json"
    path.write_text("{invalid json", encoding="utf-8")
    with pytest.raises(ValueError, match="Could not read JSON"):
        load_income(path)
