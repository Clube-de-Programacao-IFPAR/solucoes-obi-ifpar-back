from typing import TypedDict

class ValidateQuestionDTO(TypedDict):
    year: str
    phase: str
    level: str
    name: str

    filename: str
    file: str