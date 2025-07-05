from dataclasses import dataclass

import httpx

from src.config.project_config import Settings
from src.users.schemas.user_schema import GoogleUserData


@dataclass
class GoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_user_info(code=code)
        async with self.async_client as client:
            user_info = await client.get(
                self.settings.GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
        return GoogleUserData(**user_info.json(), access_token=access_token)

    async def _get_user_info(self, code: str) -> dict:
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_SECRET_KEY,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_type",
        }
        async with self.async_client as client:
            response = await client.post(
                url=self.settings.GOOGLE_REDIRECT_URI, data=data
            )
        return response.json()["access_token"]
