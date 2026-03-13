from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", backref="predictions")

    # Core ML output
    global_prob  = Column(Float, nullable=False)
    dti_ratio    = Column(Float, nullable=False)
    approved     = Column(Integer, nullable=False)   # 1 if prob >= 0.5 and dti <= 0.5

    # Request snapshot (for analytics)
    loan_purpose              = Column(String(32))
    loan_amount_requested_uzs = Column(Float)
    loan_term_months          = Column(Integer)
    monthly_income_uzs        = Column(Float)
    employment_type           = Column(String(32))
    credit_history_status     = Column(String(16))

    # Top match
    top_bank_slug    = Column(String(32))
    top_bank_score   = Column(Float)

    # Programs triggered — stored as JSON list of program_ids
    programs_triggered = Column(JSON, default=list)

    # Eligible bank count
    eligible_bank_count = Column(Integer, default=0)
