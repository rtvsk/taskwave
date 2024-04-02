from fastapi import HTTPException, status
from src.exceptions import NotFoundException


class TasksGroupNotFound(NotFoundException):
    def __init__(self, detail: str = "Tasks group not found"):
        super().__init__(detail=detail)


class UserNotOwner(HTTPException):
    def __init__(self, detail: str = "User not owner"):
        super().__init__(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=detail)
