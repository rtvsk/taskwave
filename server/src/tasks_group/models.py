import uuid

from sqlalchemy import Column, String, Boolean, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database import Base
from src.users.models import User


class TasksGroup(Base):
    __tablename__ = "tasks_group"

    def __repr__(self) -> str:
        return f"Tasks group: {self.title}"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True,
    )
    is_done = Column(Boolean(), default=False)
    title = Column(String, nullable=False)
    description = Column(String)
    deadline = Column(Date)
    author_id = Column(
        UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )

    author = relationship("User", back_populates="tasks_groups")
    tasks = relationship(
        "Task", back_populates="tasks_group", cascade="all, delete-orphan"
    )
