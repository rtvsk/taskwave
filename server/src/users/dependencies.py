from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.service import UserService
from src.database import get_async_session


def get_user_service(session: AsyncSession = Depends(get_async_session)):
    return UserService(session=session)
