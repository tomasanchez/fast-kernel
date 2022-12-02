from typing import TypeVar

from kafka import KafkaConsumer

from app.scehmas.base import CamelCaseModel

T = TypeVar("T", bound=CamelCaseModel)


class JsonCamelCaseEncoder:
    enconding = "utf-8"

    def encode(self, obj: T) -> bytes:
        return obj.json(by_alias=True, exclude_none=True).encode(encoding=self.enconding)

    def decode(self, data: str) -> T:
        return T.parse_raw(data, encoding=self.enconding)


class KafkaService:
    INSTRUCTION_KAFKA_TOPIC = "instructions"
    port = "29092"
    encoder = JsonCamelCaseEncoder()
    consumer = KafkaConsumer(
        INSTRUCTION_KAFKA_TOPIC,
        bootstrap_servers=f"localhost:{port}",
        auto_offset_reset='earliest',
        consumer_timeout_ms=10000,
        group_id=None,
    )

    def consume(self):
        print("Consuming...")
        for message in self.consumer:
            print(message.value.decode("utf-8"))
        print("Done consuming")
