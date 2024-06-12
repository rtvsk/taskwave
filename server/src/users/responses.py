from pydantic import BaseModel


class UserNotFoundException(BaseModel):
    code: int = 404
    detail: str = "User not found"
