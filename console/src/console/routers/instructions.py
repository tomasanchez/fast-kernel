from fastapi import APIRouter, Depends, HTTPException, UploadFile
from src.console.dependencies import get_kafka_service, get_parser_service
from src.console.domain.schemas import Instruction
from src.console.services.file_parser_service import FileParserService
from src.console.services.kafka_service import KafkaService

router = APIRouter(
    prefix="/instructions",
    tags=["instructions"],
    responses={500: {"description": "Kafka Connection Error"}},
)


@router.post("/")
async def create_instruction(instructions: list[Instruction], ks: KafkaService = Depends(get_kafka_service)):
    """
    Publishes a list of instructions into a message queue. It will be consumed by a Kernel consumer.
    """
    try:
        exit_instruction = Instruction(name="EXIT")

        if exit_instruction not in instructions:
            instructions.append(exit_instruction)
        else:
            instructions = instructions[:instructions.index(exit_instruction) + 1]

        await ks.publish(instructions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload",
             response_model=list[Instruction],
             responses={400: {"description": "Invalid file content"}},
             response_description="A parsed list of instructions")
async def push_instructions_from_file(file: UploadFile, parser: FileParserService = Depends(get_parser_service)):
    """
    Loads a file with instructions and publishes them into a message queue. It will be consumed by a Kernel consumer.

    It must be a txt file in which each line represent an instruction. EXIT must be the last instruction. e.g:

    NO_OP 1

    WRITE 2 3

    READ 3

    COPY 3 4

    EXIT

    """
    try:
        instructions = await parser.parse(file)
        return instructions
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
