class DeliveryBrokerMessageError(Exception):
    def __init__(self, error: str):
        self.details = f"Kafka message delivery failed: {error}"
