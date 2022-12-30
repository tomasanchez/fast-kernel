import random

import pytest

from src.console.domain.schemas import InstructionType
from src.console.services.file_parser_service import FileParserService


class TestParserService:
    parser = FileParserService()

    single_parameters = ['READ', 'NO_OP', 'IO']
    double_parameters = ['WRITE', 'COPY']

    def test_parse_valid_exit_ok(self):
        instruction = self.parser.parse_line("EXIT")
        assert instruction.name == InstructionType.EXIT
        assert instruction.params == []

    def test_parse_invalid_exit_throws_value_error(self):
        with pytest.raises(ValueError):
            self.parser.parse_line("EXIT 1 2 3")

    def test_parse_valid_single_parameter_ok(self):
        param1 = 1
        instruction = self.parser.parse_line(f"{random.choice(self.single_parameters)} {param1}")
        assert instruction.name in [InstructionType.READ, InstructionType.NO_OP, InstructionType.IO]
        assert instruction.params == [param1]

    def test_parse_invalid_single_parameter_throws_value_error(self):
        with pytest.raises(ValueError):
            self.parser.parse_line("READ")

    def test_parse_valid_double_parameter_ok(self):
        param1 = 1
        param2 = 2
        instruction = self.parser.parse_line(f"{random.choice(self.double_parameters)} {param1} {param2}")
        assert instruction.name in [InstructionType.WRITE, InstructionType.COPY]
        assert instruction.params == [param1, param2]

    def test_parse_invalid_double_parameter_throws_value_error(self):
        with pytest.raises(ValueError):
            self.parser.parse_line("WRITE 1 2 3 4 5 6")
