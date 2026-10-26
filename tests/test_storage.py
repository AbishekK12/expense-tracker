from tracker import storage


def test_save_and_load_expenses(tmp_path, monkeypatch):
    test_file = tmp_path / "test_expenses.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    expenses = [
        {
            "expense_id": 1,
            "name": "Lunch",
            "amount": 150.0,
            "category": "Food",
            "date": "2026-10-26",
        }
    ]

    storage.save_expenses(expenses)

    result = storage.load_expenses()

    assert result == expenses


def test_load_expenses_when_file_does_not_exist(tmp_path, monkeypatch):
    test_file = tmp_path / "missing.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    assert storage.load_expenses() == []


def test_load_expenses_when_json_is_invalid(tmp_path, monkeypatch):
    test_file = tmp_path / "invalid.json"
    test_file.write_text("{invalid json}", encoding="utf-8")
    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    assert storage.load_expenses() == []