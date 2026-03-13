from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProfileCreate(BaseModel):
    # Demographics
    age: int
    gender: str
    region: Optional[str] = None
    marital_status: Optional[str] = None
    dependents_count: int = 0
    is_young_family: bool = False

    # Employment
    employment_type: str
    profession_category: Optional[str] = None
    profession_role: Optional[str] = None
    salary_bank: str = "none"
    work_experience_months: int = 0

    # Income
    monthly_income_uzs: float
    has_additional_income: bool = False
    additional_income_uzs: float = 0
    income_proof_type: str = "none"

    # Financial profile
    existing_debt_monthly_uzs: float = 0
    credit_history_status: str = "none"
    has_collateral: bool = False
    collateral_type: str = "none"
    collateral_value_uzs: float = 0
    has_guarantor: bool = False
    savings_uzs: float = 0

    # Loan request
    loan_purpose: Optional[str] = None
    loan_amount_requested_uzs: Optional[float] = None
    loan_term_months: Optional[int] = None
    preferred_currency: str = "uzs"

    # Special program flags
    is_student: bool = False
    is_mahalla_low_income: bool = False
    is_women_entrepreneur: bool = False
    is_youth_entrepreneur: bool = False
    is_farmer: bool = False
    teacher_qualification_category: str = "none"
    teacher_experience_years: int = 0


class ProfileUpdate(ProfileCreate):
    pass


class ProfileRead(ProfileCreate):
    id: int
    user_id: int
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
