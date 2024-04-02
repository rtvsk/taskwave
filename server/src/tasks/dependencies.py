from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.tasks.service import TaskService
from src.database import get_async_session


def get_task_service(session: AsyncSession = Depends(get_async_session)):
    return TaskService(session=session)
