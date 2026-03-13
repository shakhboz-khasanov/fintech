from sqlalchemy import Column, Integer, String, Float, Boolean, JSON
from app.database import Base


class BankProduct(Base):
    __tablename__ = "bank_products"

    id           = Column(Integer, primary_key=True, index=True)
    bank_name    = Column(String(64), nullable=False)
    bank_slug    = Column(String(32), nullable=False, index=True)
    product_name = Column(String(128), nullable=False)
    is_active    = Column(Boolean, default=True, nullable=False)

    # Loan parameters
    loan_purposes    = Column(JSON, nullable=False)   # list of strings
    rate_min         = Column(Float, nullable=False)
    rate_max         = Column(Float, nullable=False)
    max_loan_uzs     = Column(Float, nullable=False)
    min_loan_uzs     = Column(Float, default=500_000)
    max_term_months  = Column(Integer, nullable=False)
    min_term_months  = Column(Integer, default=1)

    # Requirements
    collateral_required           = Column(Boolean, default=False)
    employment_types_required     = Column(JSON, default=list)
    employment_types_preferred    = Column(JSON, default=list)
    profession_categories_required = Column(JSON, default=list)
    profession_categories_preferred = Column(JSON, default=list)
    gender_required               = Column(String(10), nullable=True)
    salary_project_banks          = Column(JSON, default=list)
    down_payment_pct              = Column(Float, nullable=True)

    # Scoring
    score_modifier = Column(Float, default=0.0)
    notes          = Column(String(256), default="")
