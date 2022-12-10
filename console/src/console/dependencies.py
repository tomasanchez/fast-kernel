from src.console.services.file_parser_service import FileParserService
from src.console.services.kafka_service import KafkaService


async def get_kafka_service():
    return KafkaService()


async def get_parser_service():
    return FileParserService()
