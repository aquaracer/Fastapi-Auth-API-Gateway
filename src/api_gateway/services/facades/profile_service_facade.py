import json
from dataclasses import dataclass

from src.api_gateway.schemas.microservice_profiles_schema import (
    UserProfileCreateSchema, UserProfileUpdateSchema)
from src.api_gateway.services.facades.external_facade_service import \
    ExternalServiceFacade
from src.config.project_config import Settings


@dataclass
class UserProfileServiceFacade:
    external_service_facade: ExternalServiceFacade
    settings: Settings

    async def create_user_profile(self, body: UserProfileCreateSchema) -> (json, int):
        body_dict = body.dict()
        body_dict["date_of_birth"] = body_dict["date_of_birth"].isoformat()

        return await self.external_service_facade.proxy_post(
            endpoint=self.settings.PROFILE_MICROSERVICE_USER_PROFILE_ENDPOINT,
            data=body_dict,
            base_url=self.settings.PROFILE_MICROSERVICE_BASE_URL,
        )

    async def get_user_profiles(
        self, radius: int, min_age: int, max_age: int
    ) -> (json, int):
        return await self.external_service_facade.proxy_get(
            endpoint=self.settings.PROFILE_MICROSERVICE_USER_PROFILE_LIST_ENDPOINT,
            params={
                "radius": radius,
                "min_age": min_age,
                "max_age": max_age,
            },
            base_url=self.settings.PROFILE_MICROSERVICE_BASE_URL,
        )

    async def update_user_profile(self, body: UserProfileUpdateSchema) -> (json, int):
        return await self.external_service_facade.proxy_patch(
            endpoint=self.settings.PROFILE_MICROSERVICE_USER_PROFILE_ENDPOINT,
            data=body.dict(),
            base_url=self.settings.PROFILE_MICROSERVICE_BASE_URL,
        )

    async def delete_user_profile(self) -> (json, int):
        return await self.external_service_facade.proxy_delete(
            endpoint=self.settings.PROFILE_MICROSERVICE_USER_PROFILE_ENDPOINT,
            base_url=self.settings.PROFILE_MICROSERVICE_BASE_URL,
        )
