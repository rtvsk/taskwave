import asyncio
import logging
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, UTC, timedelta

from src.database import async_session_maker
from src.celeryconfig import app
from src.users.models import User
from src.tasks_group.models import TasksGroup
from src.util.email_util import email


logger = logging.getLogger(__name__)


async def get_users_from_db(session: AsyncSession) -> list[User]:
    result = await session.execute(
        select(User).where(and_(User.is_active, User.is_verified))
    )
    users = result.scalars().all()
    return users


async def get_tasksgroup_from_db(session: AsyncSession) -> list[TasksGroup]:
    result = await session.execute(
        select(TasksGroup).where(
            and_(
                TasksGroup.deadline == datetime.now(UTC).date() + timedelta(days=3),
                TasksGroup.is_done == False,
            )
        )
    )
    tasks_groups = result.scalars().all()
    return tasks_groups


async def create_bond(session: AsyncSession) -> dict[User, str]:
    tasks_groups = await get_tasksgroup_from_db(session)
    bond = {}
    if tasks_groups:
        available_users = await get_users_from_db(session)
        for task in tasks_groups:
            for user in available_users:
                if task.author_id == user.id:
                    bond[user] = task.title
    return bond


async def send_reminder_letter() -> None:
    async with async_session_maker() as session:
        user_task = await create_bond(session)
        for user, task in user_task.items():
            try:
                await email.send_reminder_letter(user, task)
                logger.debug(f"Sent mail to {user.email} for task {task}")
            except Exception as e:
                logger.error(f"Failed to send email to {user.email}: {e}")


@app.task
def send_letter() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_reminder_letter())
