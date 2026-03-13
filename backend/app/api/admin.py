from collections import Counter, defaultdict
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.deps import get_db, require_admin
from app.models.user import User
from app.models.prediction import Prediction
from app.models.bank_product import BankProduct
from app.schemas.admin import (
    AdminStats, TrendPoint, PurposeStat, BankStat,
    ProgramStat, UserListItem, BankProductRead, BankProductUpdate,
)

router = APIRouter(prefix="/admin", tags=["admin"])


# ── Stats ─────────────────────────────────────────────────────────────────────

@router.get("/stats", response_model=AdminStats)
def get_stats(
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    total_users = db.query(func.count(User.id)).scalar()
    total_preds = db.query(func.count(Prediction.id)).scalar()
    approved    = db.query(func.count(Prediction.id)).filter(Prediction.approved == 1).scalar()
    rejected    = total_preds - approved

    avg_dti    = db.query(func.avg(Prediction.dti_ratio)).scalar() or 0
    avg_income = db.query(func.avg(Prediction.monthly_income_uzs)).scalar() or 0
    avg_loan   = db.query(func.avg(Prediction.loan_amount_requested_uzs)).scalar() or 0

    return AdminStats(
        total_users=total_users,
        total_predictions=total_preds,
        approved_count=approved,
        rejected_count=rejected,
        approval_rate=round(approved / total_preds, 4) if total_preds else 0,
        avg_dti=round(avg_dti, 4),
        avg_income_uzs=round(avg_income, 2),
        avg_loan_amount_uzs=round(avg_loan, 2),
    )


# ── Trends ────────────────────────────────────────────────────────────────────

@router.get("/trends", response_model=list[TrendPoint])
def get_trends(
    days: int = 30,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    since = datetime.utcnow() - timedelta(days=days)
    preds = (
        db.query(Prediction)
        .filter(Prediction.created_at >= since)
        .all()
    )

    buckets: dict[str, dict] = defaultdict(lambda: {"total": 0, "approved": 0})
    for p in preds:
        day = p.created_at.strftime("%Y-%m-%d")
        buckets[day]["total"] += 1
        buckets[day]["approved"] += p.approved

    result = []
    for day in sorted(buckets):
        b = buckets[day]
        result.append(TrendPoint(
            date=day,
            total=b["total"],
            approved=b["approved"],
            approval_rate=round(b["approved"] / b["total"], 4) if b["total"] else 0,
        ))
    return result


# ── Loan purposes ─────────────────────────────────────────────────────────────

@router.get("/purposes", response_model=list[PurposeStat])
def get_purposes(
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Prediction.loan_purpose, func.count(Prediction.id).label("cnt"))
        .filter(Prediction.loan_purpose != None)
        .group_by(Prediction.loan_purpose)
        .order_by(func.count(Prediction.id).desc())
        .all()
    )
    total = sum(r.cnt for r in rows)
    return [
        PurposeStat(
            loan_purpose=r.loan_purpose,
            count=r.cnt,
            pct=round(r.cnt / total * 100, 2) if total else 0,
        )
        for r in rows
    ]


# ── Popular banks ─────────────────────────────────────────────────────────────

@router.get("/banks/popular", response_model=list[BankStat])
def get_popular_banks(
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Prediction.top_bank_slug, func.count(Prediction.id).label("cnt"))
        .filter(Prediction.top_bank_slug != None)
        .group_by(Prediction.top_bank_slug)
        .order_by(func.count(Prediction.id).desc())
        .all()
    )

    # Enrich with bank_name from bank_products table
    slug_to_name = {
        bp.bank_slug: bp.bank_name
        for bp in db.query(BankProduct).all()
    }

    return [
        BankStat(
            bank_slug=r.top_bank_slug,
            bank_name=slug_to_name.get(r.top_bank_slug, r.top_bank_slug),
            eligible_count=r.cnt,
            top_match_count=r.cnt,
        )
        for r in rows
    ]


# ── Special programs ──────────────────────────────────────────────────────────

@router.get("/programs", response_model=list[ProgramStat])
def get_programs(
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    preds = db.query(Prediction.programs_triggered).all()
    counter: Counter = Counter()
    total_preds = len(preds)

    for (programs,) in preds:
        if programs:
            for pid in programs:
                counter[pid] += 1

    return [
        ProgramStat(
            program_id=pid,
            count=cnt,
            pct=round(cnt / total_preds * 100, 2) if total_preds else 0,
        )
        for pid, cnt in counter.most_common()
    ]


# ── Users ─────────────────────────────────────────────────────────────────────

@router.get("/users", response_model=list[UserListItem])
def get_users(
    skip: int = 0,
    limit: int = 100,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    users = (
        db.query(User)
        .order_by(User.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    pred_counts = dict(
        db.query(Prediction.user_id, func.count(Prediction.id))
        .group_by(Prediction.user_id)
        .all()
    )

    result = []
    for u in users:
        result.append(UserListItem(
            id=u.id,
            username=u.username,
            is_admin=u.is_admin,
            created_at=u.created_at,
            last_active_at=u.last_active_at,
            prediction_count=pred_counts.get(u.id, 0),
        ))
    return result


# ── Bank products ─────────────────────────────────────────────────────────────

@router.get("/banks", response_model=list[BankProductRead])
def get_all_bank_products(
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return (
        db.query(BankProduct)
        .order_by(BankProduct.bank_name, BankProduct.product_name)
        .all()
    )


@router.put("/banks/{product_id}", response_model=BankProductRead)
def update_bank_product(
    product_id: int,
    req: BankProductUpdate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    product = db.query(BankProduct).filter(BankProduct.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Bank product not found")

    update_data = req.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product
