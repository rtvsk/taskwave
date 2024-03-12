import asyncio
from typing import AsyncGenerator
from datetime import timedelta
from collections import namedtuple
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.database import get_async_session
from src.database import Base
from src.auth.service import create_access_token
from src.config import (
    DB_HOST_TEST,
    DB_NAME_TEST,
    DB_PASS_TEST,
    DB_PORT_TEST,
    DB_USER_TEST,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from src.main import app
from src.users.models import Users


# DATABASE
DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool, echo=True)
async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def create_test_tasks_group_in_db(): ...


@pytest.fixture(scope="session")
async def create_test_user_in_db():
    async with async_session_maker() as session:
        user = Users(
            name="test_name",
            surname="test_surname",
            username="test_username",
            email="test_email@test.test",
            hashed_password=pwd_context.hash("passwordtest1"),
        )
        session.add(user)
        await session.commit()
        yield user.id


@pytest.fixture(scope="session")
def created_test_access_token() -> dict[str:str]:
    access_token = create_access_token(
        data={"sub": "john_doe"},
        expires_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)),
    )
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture(scope="function")
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def get_first_from_db(ac: AsyncClient, get_db):
    async def _get_first_from_db(model):
        async with async_session_maker() as session:
            stmt = select(model).limit(1)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    return _get_first_from_db


@pytest.fixture(scope="function")
async def get_entity_from_db(ac: AsyncClient, get_db):
    async def _get_entity_from_db(model, field_name: str, field_value: str):
        async with async_session_maker() as session:
            stmt = select(model).where(getattr(model, field_name) == field_value)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    return _get_entity_from_db


UserData = namedtuple("UserData", ["name", "surname", "username", "email", "password"])


@pytest.fixture
def john_doe_data():
    return UserData("John", "Doe", "john_doe", "john.doe@example.com", "password123")
