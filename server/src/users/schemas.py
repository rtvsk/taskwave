import uuid
import re

from pydantic import BaseModel
from pydantic import EmailStr, field_validator
from typing import Optional
from fastapi import HTTPException, status


class CreateUser(BaseModel):
    name: str
    surname: str
    username: str
    email: EmailStr
    password: str

    @field_validator("name")
    def validate_name(cls, value):
        if not re.compile(r"^[а-яА-Яa-zA-Z\-]+$").match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Name should contains only letters",
            )
        return value

    @field_validator("username")
    def validate_username(cls, value):
        if len(value) < 4:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Username must be at least 4 characters long",
            )

        if not re.search(r"[а-яА-Яa-zA-Z]", value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Username  must contains at least one letter",
            )
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password must be at least 8 characters long",
            )

        if not re.search(r"\d", value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password must contains at least one digit",
            )
        return value


class ShowUser(BaseModel):
    id: uuid.UUID
    username: str
    name: str
    surname: str
    email: EmailStr

    class Config:
        from_attributes = True


class UpdateUser(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None

    @field_validator("name")
    def validate_name(cls, value):
        if not re.compile(r"^[а-яА-Яa-zA-Z\-]+$").match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Name should contains only letters",
            )
        return value

    @field_validator("surname")
    def validate_surname(cls, value):
        if not re.compile(r"^[а-яА-Яa-zA-Z\-]+$").match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class DeletedUser(BaseModel):
    id: uuid.UUID
    username: str
