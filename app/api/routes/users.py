from fastapi import APIRouter, Depends

from app.api.deps import current_active_user
from app.schemas import UserReadSchema
from app.models import UserModel

router = APIRouter()


@router.get("/me")
async def get_current_user(
    user: UserModel = Depends(current_active_user),
) -> UserReadSchema:
    return user
