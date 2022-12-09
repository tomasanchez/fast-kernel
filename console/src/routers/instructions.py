from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_kafka_service
from app.scehmas.instruction import Instruction
from app.services.kafka_service import KafkaService

router = APIRouter(
    prefix="/instructions",
    tags=["instructions"],
    responses={500: {"description": "Kafka Connection Error"}},
)


@router.post("/")
async def create_instruction(instructions: list[Instruction], ks: KafkaService = Depends(get_kafka_service)):
    """
    Publishes an instruction into a message queue. It will be consumed by a Kernel consumer.
    """
    try:
        await ks.publish(instructions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
