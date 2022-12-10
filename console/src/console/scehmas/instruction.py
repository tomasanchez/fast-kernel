"""
 Instructions Schema
"""
from enum import Enum, auto

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
