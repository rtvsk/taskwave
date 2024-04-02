import uuid
import re

from pydantic import BaseModel
from pydantic import EmailStr, field_validator

from src.exceptions import UnprocessableException


class CreateUser(BaseModel):
    login: str
    email: EmailStr
    password: str

    @field_validator("login")
    def validate_login(cls, value):
        if len(value) < 4:
            raise UnprocessableException(
                detail="Login must be at least 4 characters long"
            )

        if not re.search(r"[а-яА-Яa-zA-Z]", value):
            raise UnprocessableException(
                detail="Login  must contains at least one letter"
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
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr

    class Config:
        from_attributes = True


class UpdateUser(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None

    @field_validator("firstname")
    def validate_firstname(cls, value):
        if not re.compile(r"^[а-яА-Яa-zA-Z\-]+$").match(value):
            raise UnprocessableException(
                detail="Firstname should contains only letters"
            )
        return value

    @field_validator("lastname")
    def validate_lastname(cls, value):
        if not re.compile(r"^[а-яА-Яa-zA-Z\-]+$").match(value):
            raise UnprocessableException(detail="Lastname should contains only letters")
        return value


class DeletedUser(BaseModel):
    id: uuid.UUID
    login: str
