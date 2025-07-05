from typing import Annotated

from fastapi import APIRouter, Depends

from src.users.dependencies.user_dependency import get_user_service
from src.users.schemas.user_schema import UserCreateSchema, UserLoginSchema
from src.users.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("", response_model=UserLoginSchema)
async def create_user(
    body: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create_user(body)
