from fastapi import UploadFile

from src.console.domain.schemas import Instruction, InstructionType


class FileParserService:

    async def parse(self, file: UploadFile) -> list[Instruction]:
        """
        Parses a file mapping it into a list of instructions
        :param file: the uploaded file
        :return: list of instructions
        """
        content = (await file.read()).decode("utf-8").strip()
        lines = content.split("\n")
        instructions = [self.parse_line(line) for line in lines]

        try:
            index = instructions.index(Instruction(name="EXIT"))
            instructions = instructions[:index + 1]
        except ValueError:
            instructions.append(Instruction(name="EXIT"))

        return instructions

    def parse_line(self, line: str):
        """
        Parses a line and returns an instruction
        :param line:
        :return:
        """
        splits: list[str] = line.strip().split(' ')
        maybe_type: str = splits[0]
        instruction_type = InstructionType(maybe_type.upper())
        self._validate_params(splits[1:])
        return Instruction(name=instruction_type, params=[int(x) for x in splits[1:]])

    @staticmethod
    def _validate_params(numbers: list[str]):
        """
        Validates whether the instruction has the correct number of fields and if the fields are valid
        :param numbers: the instruction parameters
        """

        for number in numbers:
            try:
                int(number)
            except ValueError:
                raise ValueError(f'Invalid number: {number}')
