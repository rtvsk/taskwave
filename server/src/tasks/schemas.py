import re

from pydantic import BaseModel, field_validator
from pydantic import validator
from fastapi import HTTPException, status


class TaskBase(BaseModel):
    title: str
    description: str | None = None

    @field_validator("title")
    def validate_title(cls, value):
        if len(value) < 1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
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
