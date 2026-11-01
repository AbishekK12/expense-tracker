import pytest
from fastapi.testclient import TestClient

from backend.api.main import app
import backend.api.routes.expenses as expense_routes
import backend.api.routes.income as income_routes
import backend.api.routes.categories as category_routes
import backend.api.routes.budgets as budget_routes
import backend.api.routes.insights as insights_routes


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(expense_routes, "EXPENSES_FILE", tmp_path / "expenses.json")
    monkeypatch.setattr(income_routes, "INCOME_FILE", tmp_path / "income.json")
    monkeypatch.setattr(category_routes, "CATEGORIES_FILE", tmp_path / "categories.json")
    monkeypatch.setattr(budget_routes, "BUDGETS_FILE", tmp_path / "budgets.json")
    monkeypatch.setattr(budget_routes, "EXPENSES_FILE", tmp_path / "expenses.json")
    monkeypatch.setattr(insights_routes, "EXPENSES_FILE", tmp_path / "expenses.json")
    monkeypatch.setattr(insights_routes, "INCOME_FILE", tmp_path / "income.json")
    return TestClient(app)


def test_category_create_and_duplicate_rejected(client):
    payload = {"name": "Food", "kind": "expense", "color": "#123456"}
    created = client.post("/api/categories", json=payload)
    assert created.status_code == 201
    assert client.get("/api/categories").json()["total"] == 1
    assert client.post("/api/categories", json=payload).status_code == 409


def test_budget_calculates_spend_from_expenses(client):
    expense = client.post("/api/expenses", json={
        "description": "Groceries", "amount": 1200,
        "category": "Food", "expense_date": "2026-11-01"
    })
    assert expense.status_code == 201
    budget = client.post("/api/budgets", json={
        "category": "Food", "month": "2026-11", "amount": 2000
    })
    assert budget.status_code == 201
    assert budget.json()["spent"] == 1200
    assert budget.json()["remaining"] == 800


def test_dashboard_combines_income_and_expenses(client):
    client.post("/api/expenses", json={
        "description": "Groceries", "amount": 1200,
        "category": "Food", "expense_date": "2026-11-01"
    })
    client.post("/api/income", json={
        "description": "Salary", "amount": 35000,
        "source": "Job", "income_date": "2026-11-01"
    })
    response = client.get("/api/dashboard/summary?month=2026-11")
    assert response.status_code == 200
    assert response.json()["balance"] == 33800


def test_reports_and_analytics_return_data(client):
    client.post("/api/expenses", json={
        "description": "Groceries", "amount": 1200,
        "category": "Food", "expense_date": "2026-11-01"
    })
    client.post("/api/income", json={
        "description": "Salary", "amount": 35000,
        "source": "Job", "income_date": "2026-11-01"
    })
    assert client.get("/api/analytics/monthly?year=2026").status_code == 200
    assert client.get("/api/analytics/categories?month=2026-11").json()["items"][0]["category"] == "Food"
    assert client.get("/api/reports").json()["net_balance"] == 33800
