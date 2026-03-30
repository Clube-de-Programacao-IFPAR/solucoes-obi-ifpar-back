from typing import TypedDict

class AdminAuthDTO(TypedDict):
    username: str
    role: str
    sub: str