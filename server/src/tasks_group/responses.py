from pydantic import BaseModel


class TaskGroupNotFoundException(BaseModel):
    code: int = 404
    detail: str = "Tasks group not found"


class UserNotOwnerException(BaseModel):
    code: int = 406
    detail: str = "User not owner"


class TaskGroupNotFoundException(BaseModel):
    code: int = 404
    detail: str = "Tasks group not found"
