from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class FinancialProfile(Base):
    __tablename__ = "financial_profiles"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="profile")

    # ── Demographics ─────────────────────────────────────────────────────────
    age              = Column(Integer, nullable=False)
    gender           = Column(String(10), nullable=False)
    region           = Column(String(64))
    marital_status   = Column(String(20))
    dependents_count = Column(Integer, default=0)
    is_young_family  = Column(Boolean, default=False)

    # ── Employment ────────────────────────────────────────────────────────────
    employment_type      = Column(String(32), nullable=False)
    profession_category  = Column(String(32))
    profession_role      = Column(String(48))
    salary_bank          = Column(String(32), default="none")
    work_experience_months = Column(Integer, default=0)

    # ── Income ────────────────────────────────────────────────────────────────
    monthly_income_uzs      = Column(Float, nullable=False)
    has_additional_income   = Column(Boolean, default=False)
    additional_income_uzs   = Column(Float, default=0)
    income_proof_type       = Column(String(32), default="none")

    # ── Financial profile ─────────────────────────────────────────────────────
    existing_debt_monthly_uzs = Column(Float, default=0)
    credit_history_status     = Column(String(16), default="none")
    has_collateral            = Column(Boolean, default=False)
    collateral_type           = Column(String(20), default="none")
    collateral_value_uzs      = Column(Float, default=0)
    has_guarantor             = Column(Boolean, default=False)
    savings_uzs               = Column(Float, default=0)

    # ── Loan request ──────────────────────────────────────────────────────────
    loan_purpose              = Column(String(32))
    loan_amount_requested_uzs = Column(Float)
    loan_term_months          = Column(Integer)
    preferred_currency        = Column(String(4), default="uzs")

    # ── Special program flags ─────────────────────────────────────────────────
    is_student             = Column(Boolean, default=False)
    is_mahalla_low_income  = Column(Boolean, default=False)
    is_women_entrepreneur  = Column(Boolean, default=False)
    is_youth_entrepreneur  = Column(Boolean, default=False)
    is_farmer              = Column(Boolean, default=False)
    teacher_qualification_category = Column(String(20), default="none")
    teacher_experience_years       = Column(Integer, default=0)
