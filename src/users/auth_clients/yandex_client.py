import json
from dataclasses import dataclass

import httpx
from fastapi import HTTPException

from src.config.project_config import Settings
from src.users.schemas.user_schema import YandexUserData


@dataclass
class YandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> YandexUserData:
        """
        Получение информации о юзере из Яндекса в 2 этапа
        1. Отправляем POST-запрос для получения yandex_access_token (не путать с access token системы)
        2. Отправляем GET-запрос с yandex_access_token для получение информации о пользователе
        """

        async with self.async_client as client:
            try:
                response = await client.post(
                    self.settings.YANDEX_TOKEN_URL,
                    data={
                        "grant_type": "authorization_code",
                        "code": code,
                        "client_id": self.settings.YANDEX_CLIENT_ID,
                        "client_secret": self.settings.YANDEX_SECRET_KEY,
                    },
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                )
                response.raise_for_status()
                access_token = response.json()["access_token"]
            except httpx.HTTPError as error:
                raise HTTPException(
                    status_code=400,
                    detail=f"HTTP error getting Yandex access token: {error}",
                )

            except json.JSONDecodeError as error:
                raise HTTPException(
                    status_code=400,
                    detail=f"JSON decoding error getting Yandex access token: {error}",
                )

            except KeyError as error:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing key in access token response: {error}",
                )

            try:
                user_info_response = await client.get(
                    self.settings.YANDEX_USER_INFO_URL,
                    headers={"Authorization": f"OAuth {access_token}"},
                )
                user_info_response.raise_for_status()
                return YandexUserData(
                    **user_info_response.json(), access_token=access_token
                )
            except httpx.HTTPError as error:
                raise HTTPException(
                    status_code=400,
                    detail=f"HTTP error getting user info from Yandex: {error}",
                )
            except json.JSONDecodeError as error:
                raise HTTPException(
                    status_code=400,
                    detail=f"JSON decoding error getting user info from Yandex: {error}",
                )
            except Exception as error:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unexpected error getting user info: {error}",
                )
