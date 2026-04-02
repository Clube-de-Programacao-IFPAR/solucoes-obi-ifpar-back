from typing import TypedDict

class AuthDTO(TypedDict):
    username: str
    role: str
    sub: str