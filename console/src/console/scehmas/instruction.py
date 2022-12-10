"""
 Instructions Schema
"""
from enum import Enum

from pydantic import validator

from .base import CamelCaseModel


class InstructionType(str, Enum):
    """
    Different instructions which will be sent to a message queue.

    EXIT    -> Only used to exit the program has no parameters
    NO_OP   -> No operation (1) [number of no operations]
    IO      -> Simulates an IO operation (1)  [the time in milliseconds]
    READ    -> Reads a value from a register (1) [memory address location]
    WRITE   -> Writes a value to a register (2) [value, memory address location]
    COPY    -> Copies a value from one register to another (2) [source address location, destination address location]
    """
    EXIT = 'EXIT'
    READ = 'READ'
    WRITE = 'WRITE'
    IO = 'IO'
    COPY = 'COPY'
    NO_OP = 'NO_OP'


class Instruction(CamelCaseModel):
    """
    Instruction Model. See InstructionType for more information about parameters.
    """
    name: InstructionType
    params: list[int] = []

    # noinspection PyMethodParameters
    @validator('params', always=True)
    def _params_validation(cls, v, values):
        """
        Validates whether the instruction has the correct number of parameters
        :param v: the instruction parameters
        :param values: the instruction case
        :return:
        """
        instruction_type = values['name']

        match instruction_type:
            case InstructionType.EXIT:
                if len(v) != 0:
                    raise ValueError(f'EXIT instruction should not have any parameters')
            case InstructionType.READ | InstructionType.NO_OP | InstructionType.IO:
                if len(v) != 1:
                    raise ValueError(f'{instruction_type} instruction should have only 1 parameter')
            case InstructionType.WRITE | InstructionType.COPY:
                if len(v) != 2:
                    raise ValueError(f'{instruction_type} instruction should have only 2 parameters')

        return v
