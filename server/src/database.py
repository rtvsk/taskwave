import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.config import settings
from src.exceptions import DatabaseException

logger = logging.getLogger(__name__)

engine = create_async_engine(settings.db.URL.get_secret_value(), echo=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with async_session_maker() as session:
            yield session
    except OSError as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise DatabaseException
