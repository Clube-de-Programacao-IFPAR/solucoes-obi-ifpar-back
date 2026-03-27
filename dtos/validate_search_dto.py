from typing import TypedDict

class ValidateSearchDTO(TypedDict, total=False):
    year: str
    phase: str
    level: str
    problem: str
