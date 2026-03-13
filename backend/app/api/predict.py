import os
import sys
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app.models.user import User
from app.models.prediction import Prediction
from app.schemas.predict import PredictRequest, PredictResponse

# ML module path
_ML_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "ml")
sys.path.insert(0, os.path.abspath(_ML_DIR))

try:
    from predict import SarfAIPredictor
    _predictor = SarfAIPredictor(model_dir=os.path.abspath(_ML_DIR))
except Exception as e:
    _predictor = None
    _predictor_error = str(e)

router = APIRouter(prefix="/predict", tags=["predict"])


@router.post("", response_model=PredictResponse)
def predict(
    req: PredictRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if _predictor is None:
        raise HTTPException(
            status_code=503,
            detail=f"ML model not loaded. Run ml/train.py first. Error: {_predictor_error}",
        )

    profile = req.model_dump()
    result = _predictor.predict(profile)

    # Determine top bank
    top_bank = None
    top_score = 0.0
    eligible_banks = [b for b in result["per_bank_scores"] if b["eligible"]]
    if eligible_banks:
        top_bank = eligible_banks[0]
        top_score = eligible_banks[0]["score"]

    # Log prediction
    prediction = Prediction(
        user_id=current_user.id,
        created_at=datetime.utcnow(),
        global_prob=result["global_approval_probability"],
        dti_ratio=result["dti_ratio"],
        approved=1 if (
            result["global_approval_probability"] >= 0.5
            and not result["dti_critical"]
        ) else 0,
        loan_purpose=req.loan_purpose,
        loan_amount_requested_uzs=req.loan_amount_requested_uzs,
        loan_term_months=req.loan_term_months,
        monthly_income_uzs=req.monthly_income_uzs,
        employment_type=req.employment_type,
        credit_history_status=req.credit_history_status,
        top_bank_slug=top_bank["bank_slug"] if top_bank else None,
        top_bank_score=top_score,
        programs_triggered=[p["program_id"] for p in result["special_programs"]],
        eligible_bank_count=result["eligible_bank_count"],
    )
    db.add(prediction)
    db.commit()

    return result
