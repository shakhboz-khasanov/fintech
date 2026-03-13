from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserListItem(BaseModel):
    id: int
    username: str
    is_admin: bool
    created_at: datetime
    last_active_at: datetime
    prediction_count: int

    model_config = {"from_attributes": True}


class AdminStats(BaseModel):
    total_users: int
    total_predictions: int
    approved_count: int
    rejected_count: int
    approval_rate: float
    avg_dti: float
    avg_income_uzs: float
    avg_loan_amount_uzs: float


class TrendPoint(BaseModel):
    date: str
    total: int
    approved: int
    approval_rate: float


class PurposeStat(BaseModel):
    loan_purpose: str
    count: int
    pct: float


class BankStat(BaseModel):
    bank_slug: str
    bank_name: str
    eligible_count: int
    top_match_count: int


class ProgramStat(BaseModel):
    program_id: str
    count: int
    pct: float


class BankProductRead(BaseModel):
    id: int
    bank_name: str
    bank_slug: str
    product_name: str
    is_active: bool
    loan_purposes: list[str]
    rate_min: float
    rate_max: float
    max_loan_uzs: float
    min_loan_uzs: float
    max_term_months: int
    collateral_required: bool
    notes: str

    model_config = {"from_attributes": True}


class BankProductUpdate(BaseModel):
    rate_min: Optional[float] = None
    rate_max: Optional[float] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None
    max_loan_uzs: Optional[float] = None
