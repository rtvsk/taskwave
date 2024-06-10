from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database import Base
from src.tasks_group.models import TasksGroup


class Task(Base):
    __tablename__ = "task"

    def __repr__(self) -> str:
        return f"Task-{self.id}-{self.title}"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    is_done = Column(Boolean(), default=False)
    deadline = Column(Date)
    tasks_group_id = Column(
        UUID(as_uuid=True),
        ForeignKey(TasksGroup.id, ondelete="CASCADE"),
        nullable=False,
    )

    tasks_group = relationship("TasksGroup", back_populates="tasks")
