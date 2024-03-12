from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.tasks.service import TasksService
from src.database import get_async_session


def tasks_service(session: AsyncSession = Depends(get_async_session)):
    return TasksService(session=session)
