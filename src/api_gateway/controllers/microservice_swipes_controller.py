from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.api_gateway.dependencies.api_gateway_dependency import get_swipe_facade_service
from src.api_gateway.exceptions.api_gateway_exceptions import DeliveryBrokerMessageError
from src.api_gateway.services.facades.swipe_facade_service import SwipeFacadeService
from src.users.dependencies.user_dependency import get_request_user_id

router = APIRouter(prefix="/swipes", tags=["swipes"])


@router.post("/process_swipes")
async def process_swipes(
        swiped_users: list[int],
        swipe_facade_service: Annotated[
            SwipeFacadeService,
            Depends(get_swipe_facade_service)
        ],
        user_id: int = Depends(get_request_user_id),
):
    try:
        await swipe_facade_service.process_swipes_by_kafka(
            swiped_users=swiped_users,
            user_id=user_id
        )
    except DeliveryBrokerMessageError as error:
        raise HTTPException(status_code=500, detail=error.details) from error
