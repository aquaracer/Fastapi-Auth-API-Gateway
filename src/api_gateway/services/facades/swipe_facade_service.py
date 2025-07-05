from dataclasses import dataclass
from typing import List

from src.api_gateway.adapters.producers.kafka_producer import BrokerProducer
from src.api_gateway.services.facades.external_facade_service import \
    ExternalServiceFacade
from src.config.project_config import Settings


@dataclass
class SwipeFacadeService:
    external_service_facade: ExternalServiceFacade
    settings: Settings
    broker_producer: BrokerProducer

    async def process_swipes_by_kafka(self, swiped_users: List[int], user_id: int):
        swipes_data = {
            "event": self.settings.EVENT_TYPE_PROCESS_SWIPES,
            "swiped_users": swiped_users,
            "user_id": user_id,
        }
        return await self.broker_producer.send_process_swipes_event(
            swipes_data=swipes_data
        )
