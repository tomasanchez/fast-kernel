from fastapi import APIRouter, Depends

from app.dependencies import get_kafka_service
from app.services.kafka_service import KafkaService

router = APIRouter(
    prefix="/instructions",
    tags=["instructions"],
    responses={400: {"description": "Invalid Instruction"}},
)


@router.post("/")
async def read(ks: KafkaService = Depends(get_kafka_service)) -> str:
    try:
        ks.consume()
        return "OK"
    except Exception as e:
        return str(e)
