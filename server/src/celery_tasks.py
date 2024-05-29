import asyncio
from sqlalchemy import select, and_

from datetime import datetime, UTC, timedelta
from src.database import async_session_maker
from src.celeryconfig import app
from src.users.models import User
from src.tasks_group.models import TasksGroup
from src.util.email_util import email


async def get_users_from_db() -> list[User]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(and_(User.is_active, User.is_verified))
        )
        users = result.fetchall()

        return [user[0] for user in users]


async def get_tasksgroup_from_db() -> list[TasksGroup]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(TasksGroup).where(
                and_(
                    TasksGroup.deadline == datetime.now(UTC).date() + timedelta(days=3),
                    TasksGroup.is_done == False,
                )
            )
        )
        tasks_groups = result.fetchall()
        print(tasks_groups)

        return [tasks_group[0] for tasks_group in tasks_groups]


async def create_bond():
    tasks_groups = await get_tasksgroup_from_db()
    bond = {}
    if tasks_groups:
        available_users = await get_users_from_db()
        for task in tasks_groups:
            for user in available_users:
                if task.author_id == user.id:
                    bond[user] = task.title
    return bond


async def send_reminder_letter() -> None:
    user_task = await create_bond()
    for user, task in user_task.items():
        try:
            await email.send_reminder_letter(user, task)

        except Exception as e:
            print(f"Something wrong: {e}")


@app.task
def send_letter() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_reminder_letter())
