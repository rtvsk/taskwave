from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.service import UsersService
from src.database import get_async_session


def users_service(session: AsyncSession = Depends(get_async_session)):
    return UsersService(session=session)
