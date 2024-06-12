from pydantic import BaseModel


class TaskNotFoundException(BaseModel):
    code: int = 404
    detail: str = "Task not found"
