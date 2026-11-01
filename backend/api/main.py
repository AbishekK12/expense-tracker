from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.config import CURRENCY_CODE, CURRENCY_SYMBOL
from backend.api.routes.budgets import router as budgets_router
from backend.api.routes.categories import router as categories_router
from backend.api.routes.expenses import router as expenses_router
from backend.api.routes.income import router as income_router
from backend.api.routes.insights import router as insights_router

app = FastAPI(
    title="PaisaFlow Expense Tracker API",
    version="1.0.0",
    description="Personal finance API for expenses, income, budgets, categories and reports. Default currency: INR.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expenses_router)
app.include_router(income_router)
app.include_router(categories_router)
app.include_router(budgets_router)
app.include_router(insights_router)


@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok", "currency": CURRENCY_CODE, "currency_symbol": CURRENCY_SYMBOL}


@app.get("/api/config", tags=["Configuration"])
def app_config():
    return {"currency": CURRENCY_CODE, "currency_symbol": CURRENCY_SYMBOL}
