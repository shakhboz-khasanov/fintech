from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app.models.user import User
from app.models.profile import FinancialProfile
from app.schemas.profile import ProfileCreate, ProfileRead, ProfileUpdate

router = APIRouter(prefix="/profile", tags=["profile"])


def _profile_to_dict(p: ProfileCreate) -> dict:
    return p.model_dump()


@router.get("", response_model=ProfileRead)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(FinancialProfile).filter(
        FinancialProfile.user_id == current_user.id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Create one first.")
    return profile


@router.post("", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
def create_profile(
    req: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = db.query(FinancialProfile).filter(
        FinancialProfile.user_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Profile already exists. Use PUT to update.",
        )

    profile = FinancialProfile(
        user_id=current_user.id,
        updated_at=datetime.utcnow(),
        **_profile_to_dict(req),
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.put("", response_model=ProfileRead)
def update_profile(
    req: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(FinancialProfile).filter(
        FinancialProfile.user_id == current_user.id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Create one first.")

    for field, value in _profile_to_dict(req).items():
        setattr(profile, field, value)
    profile.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(profile)
    return profile
