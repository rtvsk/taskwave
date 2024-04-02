from src.exceptions import NotFoundException
from fastapi import HTTPException, status


class UserAlreadyExists(HTTPException):
    def __init__(self, detail: str = "User already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class UserNotFound(NotFoundException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(detail=detail)
