import asyncio
import json
from typing import TypeVar, Type

from aiokafka import AIOKafkaConsumer

from app.scehmas.base import CamelCaseModel
from app.scehmas.instruction import Instruction

T = TypeVar("T", bound=CamelCaseModel)


class JsonCamelCaseEncoder:
    enconding = "utf-8"

    def __init__(self, kind: Type[T] = Instruction):
        self.kind = kind

    def encode(self, obj: T) -> bytes:
        return obj.json(by_alias=True, exclude_none=True).encode(encoding=self.enconding)

    def decode(self, data: str) -> T:
        return self.kind.parse_raw(data, encoding=self.enconding)


class KafkaService:
    INSTRUCTION_KAFKA_TOPIC = "instructions"
    port = "29092"
    encoder = JsonCamelCaseEncoder(kind=Instruction)
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer(
        INSTRUCTION_KAFKA_TOPIC,
        bootstrap_servers=f"localhost:{port}",
        auto_offset_reset='earliest',
        consumer_timeout_ms=10000,
        group_id=None,
        loop=loop)

    async def consume(self):
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                msg_decoded = json.loads(msg.value.decode(encoding="utf-8"))

                if isinstance(msg_decoded, list):
                    msg_decoded = [self.encoder.decode(data) for data in msg_decoded]
                else:
                    msg_decoded = self.encoder.decode(json.dumps(msg_decoded))

                print(f"Consumed: ({msg_decoded})")
        finally:
            await self.consumer.stop()
