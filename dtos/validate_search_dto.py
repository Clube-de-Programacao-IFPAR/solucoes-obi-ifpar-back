from ..errors.missing_field import MissingField
from ..errors.invalid_field import InvalidField

class ValidateSearchDTO:
    def __init__(
            self, 
            year: str,
            phase: str,
            level: str,
            problem: str
        ):
            self.year = year
            self.phase = phase
            self.level = level
            self.problem = problem
        
            self.validate()

    def validate(self):
        if self.year and not self.year.isdigit():
            raise InvalidField("Invalid year format")

        if self.phase and self.phase not in ("c", "1", "2", "3"):
            raise InvalidField("Invalid phase format")

        if self.level and self.level not in ("j", "1", "2", "s", "u"):
            raise InvalidField("Invalid level format")
