import httpx
from fastapi import Depends, HTTPException, Security, security
from sqlalchemy.orm import Session

from src.config.database.accessor import get_db_session
from src.config.project_config import Settings
from src.users.auth_clients.google_client import GoogleClient
from src.users.auth_clients.yandex_client import YandexClient
from src.users.exceptions.user_exceptions import TokenExpired, TokenNotCorrect
from src.users.repositories.user_repository import UserRepository
from src.users.services.auth_service import AuthService
from src.users.services.user_service import UserService


async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


async def get_user_repository(
    db_session: Session = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_google_client(
    async_client: httpx.AsyncClient = Depends(get_async_client),
) -> GoogleClient:
    return GoogleClient(settings=Settings(), async_client=async_client)


async def get_yandex_client(
    async_client: httpx.AsyncClient = Depends(get_async_client),
) -> YandexClient:
    return YandexClient(settings=Settings(), async_client=async_client)


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    google_client: GoogleClient = Depends(get_google_client),
    yandex_client: YandexClient = Depends(get_yandex_client),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
    )


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()


async def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> None:
    try:
        auth_service.get_user_id_from_access_token(token.credentials)

    except TokenExpired as error:
        raise HTTPException(status_code=401, detail=error.detail)

    except TokenNotCorrect as error:
        raise HTTPException(status_code=401, detail=error.detail)
