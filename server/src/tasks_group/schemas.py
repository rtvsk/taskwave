import uuid
from datetime import date

from pydantic import BaseModel
from pydantic import field_validator

from src.exceptions import UnprocessableException


class TasksGroupBase(BaseModel):
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


class CreateTasksGroup(TasksGroupBase):
    pass


class ShowTasksGroup(TasksGroupBase):
    id: uuid.UUID


class UpdateTasksGroup(TasksGroupBase):
    title: str | None = None
    is_done: bool | None = None
