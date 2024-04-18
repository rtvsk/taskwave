from datetime import date
from pydantic import BaseModel, field_validator
from src.exceptions import UnprocessableException


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    deadline: date | None = None

    @field_validator("title")
    def validate_title(cls, value):
        if len(value) < 1:
            raise UnprocessableException(
                detail="Title must contains at least one simbol"
            )
        return value


class ShowTask(TaskBase):
    id: int
    is_done: bool


class CreateTask(TaskBase):
    pass


class UpdateTask(TaskBase):
    title: str | None = None
    is_done: bool | None = None
    deadline: date | None = None
