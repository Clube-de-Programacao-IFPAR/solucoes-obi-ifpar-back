from typing import TypedDict

class Validate_question_dto(TypedDict):
    year: str
    phase: str
    level: str
    name: str

    filename: str
    file: str