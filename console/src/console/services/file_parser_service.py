from src.console.scehmas.instruction import Instruction, InstructionType


class FileParserService:

    def parse(self, file_path) -> list[Instruction]:
        """
        Parses a file mapping it into a list of instructions
        :param file_path: path to the file
        :return: list of instructions
        """
        with open(file_path, 'r', encoding="utf-8") as file:
            instructions = [self.parse_line(line) for line in file]
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
        self._validate_fields(instruction_type, splits)
        return Instruction(name=instruction_type, params=[int(x) for x in splits[1:]])

    @staticmethod
    def _validate_fields(instruction_type: InstructionType, splits: list[str]):
        """
        Validates whether the instruction has the correct number of fields and if the fields are valid
        :param instruction_type: the instruction case
        :param splits: the instruction parameters
        :return:
        """
        numbers = splits[1:]

        for number in numbers:
            try:
                int(number)
            except ValueError:
                raise ValueError(f'Invalid number: {number}')

        match instruction_type:
            case InstructionType.EXIT:
                if len(splits) != 1:
                    raise ValueError(f'EXIT instruction should not have any parameters')
            case InstructionType.READ | InstructionType.NO_OP | InstructionType.IO:
                if len(splits) != 2:
                    raise ValueError(f'{instruction_type} instruction should have 1 parameter')
            case InstructionType.WRITE | InstructionType.COPY:
                if len(splits) != 3:
                    raise ValueError(f'{instruction_type} instruction should have 2 parameters')
