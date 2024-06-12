from pydantic import BaseModel


class UserAlreadyExistsException(BaseModel):
    code: int = 409
    detail: str = "User with this login or email already exists"


class SigninException(BaseModel):
    code: int = 401
    detail: str = "Incorrect login or password"


class InvalidLinkException(BaseModel):
    code: int = 404
    detail: str = "Invalid link"
