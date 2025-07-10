from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from src.users.dependencies.user_dependency import get_auth_service
from src.users.exceptions.user_exceptions import (
    UserNotCorrectPasswordExceptionError,
    UserNotFoundExceptionError,
)
from src.users.schemas.user_schema import UserCreateSchema, UserLoginSchema
from src.users.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("", response_model=UserLoginSchema)
async def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        return await auth_service.login(body.username, body.password)

    except UserNotFoundExceptionError as error:
        raise HTTPException(status_code=404, detail=error.details) from error

    except UserNotCorrectPasswordExceptionError as error:
        raise HTTPException(status_code=401, detail=error.details) from error


@router.get("/login/google", response_class=RedirectResponse)
async def google_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    redirect_url = auth_service.get_google_redirect_url()
    return RedirectResponse(redirect_url)


@router.get("/google", response_model=UserLoginSchema)
async def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str
):
    return await auth_service.google_auth(code=code)


@router.get("/login/yandex", response_class=RedirectResponse)
async def yandex_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    redirect_url = auth_service.get_yandex_redirect_url()
    return RedirectResponse(redirect_url)


@router.get("/yandex", response_model=UserLoginSchema)
async def yandex_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str
):
    return await auth_service.yandex_auth(code=code)
