from fastapi import APIRouter, Depends

from app.dependencies import get_kafka_service
from app.scehmas.instruction import Instruction
from app.services.kafka_service import KafkaService

router = APIRouter(
    prefix="/instructions",
    tags=["instructions"],
    responses={400: {"description": "Invalid Instruction"}},
)


@router.post("/")
async def create_instruction(instruction: Instruction, ks: KafkaService = Depends(get_kafka_service)) -> str:
    try:
        ks.publish(instruction)
        return "OK"
    except Exception as e:
        return str(e)
