import json
from dataclasses import dataclass

from aiokafka import AIOKafkaProducer

from src.api_gateway.exceptions.api_gateway_exceptions import DeliveryBrokerMessageError


@dataclass
class BrokerProducer:
    producer: AIOKafkaProducer
    process_swipes_topic: str

    async def open_connection(self) -> None:
        await self.producer.start()

    async def close_connection(self) -> None:
        await self.producer.stop()

    async def send_process_swipes_event(self, swipes_data: dict) -> None:
        encode_swipes_data = json.dumps(swipes_data).encode()
        await self.open_connection()
        try:
            await self.producer.send(topic=self.process_swipes_topic,
                                     value=encode_swipes_data)
        except Exception as error:
            raise DeliveryBrokerMessageError(error) from error
        finally:
            await self.close_connection()
