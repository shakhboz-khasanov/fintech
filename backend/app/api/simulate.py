from fastapi import APIRouter, Depends
from app.deps import get_current_user
from app.models.user import User
from app.schemas.simulate import SimulateRequest, SimulateResponse
from app.services.simulation import run_simulation

router = APIRouter(prefix="/simulate", tags=["simulate"])


@router.post("", response_model=SimulateResponse)
def simulate(
    req: SimulateRequest,
    current_user: User = Depends(get_current_user),
):
    return run_simulation(req)
