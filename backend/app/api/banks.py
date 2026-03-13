from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models.bank_product import BankProduct
from app.schemas.admin import BankProductRead

router = APIRouter(prefix="/banks", tags=["banks"])


@router.get("", response_model=list[BankProductRead])
def list_banks(db: Session = Depends(get_db)):
    products = (
        db.query(BankProduct)
        .filter(BankProduct.is_active == True)
        .order_by(BankProduct.bank_name, BankProduct.product_name)
        .all()
    )
    return products
