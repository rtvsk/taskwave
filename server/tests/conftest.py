import pytest

from datetime import timedelta
from typing import AsyncGenerator
from collections import namedtuple

from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.database import get_async_session
from src.database import Base
from src.config import DATABASE_URL_TEST
from src.main import app

from src.auth.jwt import create_access_token


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


@pytest.fixture(autouse=True, scope="session")
def created_test_access_token() -> dict[str:str]:
    access_token = create_access_token(
        data={"sub": "john_doe"},
        expires_delta=timedelta(minutes=30),
    )
    return {"Authorization": f"Bearer {access_token}"}


client = TestClient(app)


@pytest.fixture(scope="session")
async def api_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as api_client:
        yield api_client


UserSignupData = namedtuple("UserSignupData", ["login", "email", "password"])

UserSigninData = namedtuple("UserSigninData", ["login", "password"])

UserUpdateData = namedtuple("UserUpdateData", ["firstname", "lastname"])


@pytest.fixture
def john_doe_signup_data():
    return UserSignupData("john_doe", "john.doe@example.com", "password123")


@pytest.fixture
def john_doe_signin_data():
    return UserSigninData("john_doe", "password123")


@pytest.fixture
def john_doe_update_data():
    return UserUpdateData("John", "Doe")


##### THINK THINK THINK #####
@pytest.fixture
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def get_first_from_db(api_client: AsyncClient, get_db):
    async def _get_first_from_db(model):
        async with async_session_maker() as session:
            stmt = select(model).limit(1)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    return _get_first_from_db


@pytest.fixture(scope="function")
async def get_entity_from_db(api_client: AsyncClient, get_db):
    async def _get_entity_from_db(model, field_name: str, field_value: str):
        async with async_session_maker() as session:
            stmt = select(model).where(getattr(model, field_name) == field_value)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    return _get_entity_from_db
