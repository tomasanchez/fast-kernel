from src.console.services.kafka_service import KafkaService


async def get_kafka_service():
    return KafkaService()
