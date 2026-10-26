from tracker.validation import (
    validate_name,
    validate_amount,
    validate_date,
)


def test_validate_name():
    assert validate_name("Lunch") is True
    assert validate_name("   ") is False


def test_validate_amount():
    assert validate_amount(150) is True
    assert validate_amount(-50) is False
    assert validate_amount(0) is False


def test_validate_date():
    assert validate_date("2026-10-26") is True
    assert validate_date("invalid") is False
    assert validate_date("2026-13-40") is False