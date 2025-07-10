from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.api_gateway.dependencies.api_gateway_dependency import (
    get_user_profile_service_facade,
)
from src.api_gateway.schemas.microservice_profiles_schema import (
    UserProfileCreateSchema,
    UserProfileUpdateSchema,
)
from src.api_gateway.services.facades.profile_service_facade import (
    UserProfileServiceFacade,
)

router = APIRouter(prefix="/user_profile", tags=["user_profile"])


@router.post("")
async def create_user_profile(
        body: UserProfileCreateSchema,
        user_profile_service_facade: Annotated[
            UserProfileServiceFacade,
            Depends(get_user_profile_service_facade)
        ],
):
    content, status_code = await user_profile_service_facade.create_user_profile(
        body=body
    )
    return JSONResponse(content=content, status_code=status_code)


@router.get("/list")
async def get_user_profiles_with_filtering(
        user_profile_service_facade: Annotated[
            UserProfileServiceFacade,
            Depends(get_user_profile_service_facade)
        ],
        radius: int,
        min_age: int,
        max_age: int,
):
    content, status_code = await user_profile_service_facade.get_user_profiles(
        radius=radius, min_age=min_age, max_age=max_age
    )
    return JSONResponse(content=content, status_code=status_code)


@router.patch("")
async def patch_user_profile(
        body: UserProfileUpdateSchema,
        user_profile_service_facade: Annotated[
            UserProfileServiceFacade,
            Depends(get_user_profile_service_facade)
        ],
):
    content, status_code = await user_profile_service_facade.update_user_profile(
        body=body
    )
    return JSONResponse(content=content, status_code=status_code)


@router.delete("")
async def delete_user_profile(
        user_profile_service_facade: Annotated[
            UserProfileServiceFacade,
            Depends(get_user_profile_service_facade)
        ],
):
    content, status_code = await user_profile_service_facade.delete_user_profile()
    return JSONResponse(content=content, status_code=status_code)
