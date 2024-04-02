import uuid

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True,
    )
    is_active = Column(Boolean(), default=True)


class User(Base):
    __tablename__ = "user"

    login = Column(String, nullable=False)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    # is_verify = Column(Boolean(), default=False)

    # tasks_group = relationship("TasksGroup", back_populates="author")


class TasksGroup(Base):
    __tablename__ = "tasks_group"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    author_id = Column(
        UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )

    # author = relationship("User", uselist=False, back_populates="tasks_group")
    # task = relationship("Task", back_populates="task")


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_done = Column(Boolean(), default=False)
    tasks_group_id = Column(
        UUID(as_uuid=True),
        ForeignKey(TasksGroup.id, ondelete="CASCADE"),
        nullable=False,
    )

    # tasks_group = relationship("TasksGroup", uselist=False, back_populates="task")
