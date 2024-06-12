from pydantic import BaseModel


class ValidationException(BaseModel):
    code: int = 422
    detail: str = "Validation error mesage"


class InvalidCredentialsException(BaseModel):
    code: int = 401
    detail: str = "Could not validate credentials"
