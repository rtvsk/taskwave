import uuid
import re

from pydantic import BaseModel
from pydantic import EmailStr, field_validator

from src.exceptions import UnprocessableException


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
