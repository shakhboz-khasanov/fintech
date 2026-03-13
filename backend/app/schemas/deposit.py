from typing import Optional
from pydantic import BaseModel


class DepositRequest(BaseModel):
    amount_uzs: Optional[float] = None
    amount_usd: Optional[float] = None
    preferred_currency: str = "uzs"
    preferred_term_months: Optional[int] = None
    needs_early_withdrawal: bool = False


class DepositMatch(BaseModel):
    bank_name: str
    bank_slug: str
    product_name: str
    currency: str
    rate_pct: float
    term_months: int
    min_amount: Optional[float]
    projected_return: Optional[float]
    notes: str
    score: float


class DepositResponse(BaseModel):
    matches: list[DepositMatch]
    best_uzs: Optional[DepositMatch] = None
    best_usd: Optional[DepositMatch] = None
    tips: list[str]
