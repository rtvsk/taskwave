import uuid

from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base
from src.users.models import Users


class TasksGroup(Base):
    __tablename__ = "tasks_group"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True,
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    author_id = Column(
        UUID(as_uuid=True),
        ForeignKey(Users.id, ondelete="CASCADE"),
        nullable=False,
    )
    is_active = Column(Boolean(), default=True)
