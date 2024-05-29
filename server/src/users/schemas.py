import uuid
import re

from pydantic import BaseModel
from pydantic import EmailStr


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


class DeletedUser(BaseModel):
    id: uuid.UUID
    login: str
