import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "user"

    def __repr__(self) -> str:
        return f"user-{self.login}"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True,
    )
    login = Column(String, nullable=False)
    firstname = Column(String)
    lastname = Column(String)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_verified = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)

    tasks_groups = relationship("TasksGroup", back_populates="author")
