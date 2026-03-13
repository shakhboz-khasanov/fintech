from fastapi import APIRouter, Depends
from app.deps import get_current_user
from app.models.user import User
from app.schemas.deposit import DepositRequest, DepositResponse
from app.services.deposit import match_deposits

router = APIRouter(prefix="/deposit", tags=["deposit"])


@router.post("/match", response_model=DepositResponse)
def deposit_match(
    req: DepositRequest,
    current_user: User = Depends(get_current_user),
):
    return match_deposits(req)
