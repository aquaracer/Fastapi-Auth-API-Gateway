from fastapi import APIRouter

from src.api_gateway.controllers.microservice_photos_controller import (
    router as photo_srvice_router,
)
from src.api_gateway.controllers.microservice_profiles_controller import (
    router as user_profile_service_router,
)
from src.api_gateway.controllers.microservice_swipes_controller import (
    router as swipe_service_router,
)
from src.users.controllers.auth_controller import router as auth_router
from src.users.controllers.user_controller import router as user_router


def get_apps_router():
    router = APIRouter()
    router.include_router(auth_router)
    router.include_router(user_router)
    router.include_router(user_profile_service_router)
    router.include_router(swipe_service_router)
    router.include_router(photo_srvice_router)
    return router
