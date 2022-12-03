import asyncio
import json
from typing import TypeVar

from aiokafka import AIOKafkaProducer

from app.scehmas.base import CamelCaseModel

T = TypeVar("T", bound=CamelCaseModel)


class JsonCamelCaseEncoder:
    encoding = "utf-8"

    def encode(self, obj: T) -> bytes:
        return obj.json(by_alias=True, exclude_none=True).encode(encoding=self.encoding)


class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')

        if isinstance(obj, CamelCaseModel):
            return JsonCamelCaseEncoder().encode(obj)

        return json.JSONEncoder.default(self, obj)


class KafkaService:
    INSTRUCTION_KAFKA_TOPIC = "instructions"

    def __init__(self, port="29092"):
        self.port = port

    @property
    def producer(self):
        return AIOKafkaProducer(
            bootstrap_servers=f"localhost:{self.port}",
        )

    async def publish(self, data: list[T]):
        producer = self.producer
        await producer.start()
        try:
            encoded_data = json.dumps(data, cls=BytesEncoder).encode(encoding="utf-8")
            await producer.send_and_wait(self.INSTRUCTION_KAFKA_TOPIC, encoded_data)
        finally:
            await producer.stop()
