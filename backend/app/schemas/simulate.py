from pydantic import BaseModel


class SimulateRequest(BaseModel):
    loan_amount_uzs: float
    annual_rate_pct: float
    term_months: int
    monthly_income_uzs: float
    monthly_expenses_uzs: float = 0
    existing_debt_monthly_uzs: float = 0


class MonthRow(BaseModel):
    month: int
    payment: float
    principal: float
    interest: float
    balance: float
    disposable_income: float
    cumulative_interest: float


class SimulateResponse(BaseModel):
    monthly_payment: float
    total_payment: float
    total_interest: float
    dti_ratio: float
    dti_warning: bool
    schedule: list[MonthRow]
