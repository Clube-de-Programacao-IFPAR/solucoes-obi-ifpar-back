from ..errors.missing_field import MissingField
from ..errors.invalid_field import InvalidField

class ValidateQuestionDTO:
    def __init__(
        self,
        year: str,
        phase: str,
        level: str,
        name: str,
        filename: str,
        file: str
    ):
        self.year = year
        self.phase = phase
        self.level = level
        self.name = name
        self.filename = filename
        self.file = file
        
        self.validate()

    def validate(self):
        if not self.year:
            raise MissingField("Missing field \"year\"")

        if not self.year.isdigit():
            raise InvalidField("Invalid field \"year\", not a number")

        if not self.phase:
            raise MissingField("Missing field \"phase\"")

        if self.phase not in ("cf", "0", "1", "2", "3"):
            raise InvalidField("Invalid field \"phase\", not in [\"cf\", \"0\", \"1\", \"2\", \"3\"]")

        if not self.level:
            raise MissingField("Missing field \"level\"")

        if self.level not in ("j", "0", "1", "2", "s", "u"):
            raise InvalidField("Invalid field \"level\", not in [\"j\", \"0\", \"1\", \"2\", \"s\", \"u\"]")

        if not self.name:
            raise MissingField("Missing field \"name\"")

        if not self.filename:
            raise MissingField("Missing field \"filename\"")

        if not self.file:
            raise MissingField("Missing field \"file\"")
