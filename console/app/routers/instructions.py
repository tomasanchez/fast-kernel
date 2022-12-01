from fastapi import APIRouter

from app.scehmas.instruction import Instruction

router = APIRouter(
    prefix="/instructions",
    tags=["instructions"],
    responses={400: {"description": "Invalid Instruction"}},
)


@router.post("/")
async def create_instruction(instruction: Instruction) -> str:
    return "OK"
