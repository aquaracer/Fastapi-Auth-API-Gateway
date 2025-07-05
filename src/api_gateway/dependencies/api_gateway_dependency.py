import asyncio
import datetime as dt

import httpx
from aiokafka import AIOKafkaProducer
from fastapi import Depends, HTTPException, Security, security
from jose import JWTError, jwt

from src.api_gateway.adapters.producers.kafka_producer import BrokerProducer
from src.api_gateway.services.facades.external_facade_service import ExternalServiceFacade
from src.api_gateway.services.facades.photo_service_facade import PhotoServiceFacade
from src.api_gateway.services.facades.profile_service_facade import UserProfileServiceFacade
from src.api_gateway.services.facades.swipe_facade_service import SwipeFacadeService
from src.config.project_config import Settings
from src.users.dependencies.user_dependency import get_async_client, reusable_oauth2

event_loop = asyncio.get_event_loop()


async def get_access_token(token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2), ):
    settings = Settings()

    try:
        payload = jwt.decode(
            token.credentials,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ENCODE_ALGORITHM],
        )
    except JWTError as error:
        raise HTTPException(status_code=401, detail="Token is not correct")

    if payload["expire"] < dt.datetime.utcnow().timestamp():
        raise HTTPException(status_code=401, detail="Token has expired")

    return token.credentials


async def get_external_service_facade(
        async_client: httpx.AsyncClient = Depends(get_async_client),
        access_token: str = Depends(get_access_token),
) -> ExternalServiceFacade:
    return ExternalServiceFacade(async_client=async_client, access_token=access_token)


async def get_broker_producer() -> BrokerProducer:
    settings = Settings()
    return BrokerProducer(
        producer=AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BROKER_ADDRESS, loop=event_loop),
        process_swipes_topic=settings.PROCESS_SWIPES_TOPIC,
    )


async def get_swipe_facade_service(
        external_service_facade: ExternalServiceFacade = Depends(get_external_service_facade),
        broker_producer: BrokerProducer = Depends(get_broker_producer),
) -> SwipeFacadeService:
    return SwipeFacadeService(
        external_service_facade=external_service_facade,
        settings=Settings(),
        broker_producer=broker_producer,
    )


async def get_photo_service_facade(
        external_service_facade: ExternalServiceFacade = Depends(
            get_external_service_facade
        ),
) -> PhotoServiceFacade:
    return PhotoServiceFacade(
        external_service_facade=external_service_facade,
        settings=Settings(),
    )


async def get_user_profile_service_facade(
        external_service_facade: ExternalServiceFacade = Depends(
            get_external_service_facade
        ),
) -> UserProfileServiceFacade:
    return UserProfileServiceFacade(
        external_service_facade=external_service_facade,
        settings=Settings(),
    )
