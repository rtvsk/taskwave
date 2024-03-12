import uuid

from pydantic import BaseModel
from src.tasks.schemas import TaskBase


class ShowTasksGroup(TaskBase):
    id: uuid.UUID


class UpdateTasksGroup(TaskBase):
    title: str | None = None


class DeletedTasksGroup(BaseModel):
    id: uuid.UUID
    title: str
