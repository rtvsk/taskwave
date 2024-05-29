from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.service import UserService
from src.database import get_async_session


def get_user_service(session: AsyncSession = Depends(get_async_session)):
    """
    Provide a UserService instance.
    """
    return UserService(session=session)
