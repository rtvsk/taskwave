import re
from pydantic import BaseModel
from pydantic import EmailStr, field_validator

from src.exceptions import UnprocessableException


class CreateUser(BaseModel):
    login: str
    password: str
    email: EmailStr

    @field_validator("login")
    def validate_login(cls, value):
        if len(value) < 4:
            raise UnprocessableException(
                detail="Login must be at least 4 characters long"
            )
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise UnprocessableException(
                detail="Password must be at least 8 characters long"
            )

        if not re.search(r"\d", value):
            raise UnprocessableException(
                detail="Password must contains at least one digit"
            )
        return value


class ShowUser(BaseModel):
    login: str


class LoginForm(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    login: str | None = None
