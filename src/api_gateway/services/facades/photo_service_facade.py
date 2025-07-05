import json
from dataclasses import dataclass
from typing import List

from fastapi import UploadFile

from src.api_gateway.services.facades.external_facade_service import \
    ExternalServiceFacade
from src.config.project_config import Settings


@dataclass
class PhotoServiceFacade:
    external_service_facade: ExternalServiceFacade
    settings: Settings

    async def upload_photos(self, files: List[UploadFile]) -> (json, int):
        return await self.external_service_facade.proxy_post(
            endpoint=self.settings.PHOTO_MICROSERVICE_PHOTO_ENDPOINT,
            data={},
            files=files,
            base_url=self.settings.PHOTO_MICROSERVICE_BASE_URL,
        )

    async def get_own_photos(self) -> (json, int):
        return await self.external_service_facade.proxy_get(
            endpoint=self.settings.PHOTO_MICROSERVICE_LIST_OWN_PHOTOS_ENDPOINT,
            base_url=self.settings.PHOTO_MICROSERVICE_BASE_URL,
        )

    async def get_users_photos(self, user_ids: List[int]) -> (json, int):
        custom_query_params = "&".join([f"user_ids={x}" for x in user_ids])
        return await self.external_service_facade.proxy_get(
            endpoint=f"{self.settings.PHOTO_MICROSERVICE_LIST_USERS_PHOTOS_ENDPOINT}{custom_query_params}",
            base_url=self.settings.PHOTO_MICROSERVICE_BASE_URL,
        )

    async def delete_photo(self, photo_id: int) -> (json, int):
        return await self.external_service_facade.proxy_delete(
            endpoint=f"{self.settings.PHOTO_MICROSERVICE_PHOTO_ENDPOINT}/{photo_id}",
            base_url=self.settings.PHOTO_MICROSERVICE_BASE_URL,
        )
