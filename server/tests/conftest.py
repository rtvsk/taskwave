import pytest
import logging

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
from src.config import settings
from src.main import app

from src.auth.jwt import JwtToken
from src.users.models import User
from src.tasks_group.models import TasksGroup
from src.tasks.models import Task


logging.basicConfig(
    level=logging.DEBUG,
    filename="test_log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

engine_test = create_async_engine(
    settings.test_db.URL.get_secret_value(), poolclass=NullPool, echo=True
)
async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session

TEST_USER = {
    "id": "cb417dbc-4c34-4028-af90-64c3b79300e2",
    "login": "Test",
    "email": "test-email34@yandex.ru",
    "hashed_password": "12345678T",
}

TEST_TASKS_GROUP = {
    "id": "0454e5e0-24fc-484b-adc2-fd3c8a46b5ee",
    "title": "testTasksGroup",
    "author_id": "cb417dbc-4c34-4028-af90-64c3b79300e2",
}

TEST_TASK = {
    "id": 99,
    "title": "testTask",
    "tasks_group_id": "0454e5e0-24fc-484b-adc2-fd3c8a46b5ee",
}


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    logger.info("Preparing database...")
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully.")

    for model, data in (
        (User, TEST_USER),
        (TasksGroup, TEST_TASKS_GROUP),
        (Task, TEST_TASK),
    ):
        async with async_session_maker() as session:
            try:
                logger.info(f"Inserting test in {model}...")
                add_data = model(**data)
                session.add(add_data)
                await session.commit()
                logger.info(f"Test {model} data inserted successfully.")
            except Exception as e:
                logger.error(f"Error inserting test: {e}")
                await session.rollback()
                logger.info("Rolled back transaction.")
    logger.info("Database preparation complete.")

    yield

    logger.info("Deleting database...")
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.info("Database tables delete successfully.")


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True, scope="session")
def created_test_access_token() -> dict[str:str]:
    access_token = JwtToken.create_access_token(data={"sub": "john_doe"})
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


##############THINK THINK THINK#############
@pytest.fixture
async def get_entity_from_db(api_client: AsyncClient):
    async def _get_entity_from_db(model, field_name: str, field_value: str):
        async with async_session_maker() as session:
            result = select(model).where(getattr(model, field_name) == field_value)
            entity = await session.execute(result)
            return entity.scalar_one_or_none()

    return _get_entity_from_db
