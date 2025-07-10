from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.params import Query
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.api_gateway.dependencies.api_gateway_dependency import get_photo_service_facade
from src.api_gateway.services.facades.photo_service_facade import PhotoServiceFacade

router = APIRouter(prefix="/photo", tags=["photo"])


@router.post("")
async def upload_photos(
        photo_service_facade: Annotated[
            PhotoServiceFacade,
            Depends(get_photo_service_facade)
        ],
        files: list[UploadFile] = File(...),
) -> JSONResponse:
    content, status_code = await photo_service_facade.upload_photos(files=files)
    return JSONResponse(content=content, status_code=status_code)


@router.get("/list_own_photos")
async def get_own_photos(
        photo_service_facade: Annotated[
            PhotoServiceFacade,
            Depends(get_photo_service_facade)
        ],
) -> JSONResponse:
    content, status_code = await photo_service_facade.get_own_photos()
    return JSONResponse(content=content, status_code=status_code)


@router.get("/list_users_photos")
async def get_users_photos(
        photo_service_facade: Annotated[
            PhotoServiceFacade,
            Depends(get_photo_service_facade)
        ],
        user_ids: Annotated[list[int] | None, Query()] = None,
) -> JSONResponse:
    content, status_code = await photo_service_facade.get_users_photos(
        user_ids=user_ids
    )
    return JSONResponse(content=content, status_code=status_code)


@router.delete("/{photo_id}")
async def delete_photo(
        photo_service_facade: Annotated[
            PhotoServiceFacade,
            Depends(get_photo_service_facade)
        ],
        photo_id: int,
        request: Request,
) -> JSONResponse:
    request.get("")
    content, status_code = await photo_service_facade.delete_photo(photo_id=photo_id)
    return JSONResponse(content=content, status_code=status_code)
