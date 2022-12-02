"""
 Instructions Schema
"""
from enum import Enum, auto

from .base import CamelCaseModel


class InstructionType(str, Enum):
    """
    Instruction Type Enum
    """
    EXIT = 'EXIT'
    READ = 'READ'
    WRITE = 'WRITE'
    IO = 'IO'
    COPY = 'COPY'
    NO_OP = 'NO_OP'


class Instruction(CamelCaseModel):
    """
    Instruction Model
    """
    name: InstructionType
    params: list[int]
