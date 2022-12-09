from fastapi import APIRouter, Depends
from fastapi import HTTPException

from app.dependencies import get_kafka_service
from app.services.kafka_service import KafkaService

router = APIRouter(
    prefix="/instructions",
    tags=["instructions"],
    responses={500: {"description": "Kafka Connection Error"}},
)


@router.post("/")
async def read(ks: KafkaService = Depends(get_kafka_service)) -> str:
    try:
        await ks.consume()
        return "OK"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
