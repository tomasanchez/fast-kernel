from typing import TypeVar

from kafka import KafkaProducer

from app.scehmas.base import CamelCaseModel

T = TypeVar("T", bound=CamelCaseModel)


class JsonCamelCaseEncoder:
    enconding = "utf-8"

    def encode(self, obj: T) -> bytes:
        return obj.json(by_alias=True, exclude_none=True).encode(encoding=self.enconding)


class KafkaService:
    INSTRUCTION_KAFKA_TOPIC = "instructions"
    port = "29092"
    encoder = JsonCamelCaseEncoder()
    producer = KafkaProducer(
        bootstrap_servers=f"localhost:{port}")

    def publish(self, data: T):
        self.producer.send(topic=self.INSTRUCTION_KAFKA_TOPIC,
                           value=self.encoder.encode(data))
        self.flush()

    def flush(self):
        self.producer.flush()
        self.producer.close()
        self.producer = KafkaProducer(
            bootstrap_servers=f"localhost:{self.port}")
