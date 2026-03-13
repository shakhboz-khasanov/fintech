from typing import Optional
from pydantic import BaseModel
from app.schemas.profile import ProfileCreate


class PredictRequest(ProfileCreate):
    """Full profile sent for prediction. Extends ProfileCreate."""
    pass


class BankScore(BaseModel):
    bank_id: int
    bank_name: str
    bank_slug: str
    product_name: str
    score: float
    eligible: bool
    ineligible_reasons: list[str]
    rate_min: float
    rate_max: float
    rate_midpoint: float
    max_loan_uzs: float
    max_term_months: int
    collateral_required: bool
    matched_programs: list[str]
    notes: str


class SpecialProgram(BaseModel):
    eligible: bool
    program_id: str
    program_name: str
    benefit: str
    applicable_banks: list[str]
    rate_discount_pct: float
    max_loan_uzs: Optional[float] = None
    collateral_required: bool = False


class PredictResponse(BaseModel):
    global_approval_probability: float
    dti_ratio: float
    dti_warning: bool
    dti_critical: bool
    max_affordable_loan_uzs: int
    per_bank_scores: list[BankScore]
    eligible_bank_count: int
    special_programs: list[SpecialProgram]
    profile_tips: list[str]
