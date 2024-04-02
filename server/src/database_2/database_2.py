from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# class Session:

#     def __init__(self):
#         self._session = async_session_maker

#     async def __aenter__(self):
#         self.session = async_session_maker()
#         # return self.session

#     async def __aexit__(self, *args):
#         await self.rollback()
#         await self.session.close()

#     async def commit(self):
#         await self.session.commit()

#     async def rollback(self):
#         await self.session.rollback()
