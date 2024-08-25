from fastapi import APIRouter

from app.core.users import fastapi_users, auth_backend
from app.schemas import UserCreateSchema, UserReadSchema

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
)

router.include_router(
    fastapi_users.get_register_router(UserReadSchema, UserCreateSchema),
)
