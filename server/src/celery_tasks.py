import asyncio
from sqlalchemy import select, and_

from datetime import datetime, UTC, timedelta
from src.database import async_session_maker
from src.celeryconfig import app
from src.users.models import User
from src.tasks_group.models import TasksGroup
from src.util.email_util import Email


async def get_users_from_db() -> list[User]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(and_(User.is_active, User.is_verified))
        )
        users = result.fetchall()

        return [user[0] for user in users]


async def send_reminder_letter() -> None:
    users = await get_users_from_db()

    for user in users:
        try:
            await Email.send_test(user)

        except Exception as e:
            print(f"Something wrooooooong: {e}")


@app.task
def send_test_email() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_reminder_letter())


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


# async def get_user_from_task(tasks) -> list[User]:
#     user_bond_task = {}

#     tasks_groups = user.tasks_groups
#     deadlines = []
#     for tasks_group in tasks_groups:
#         tasks = tasks_group.tasks
#         for task in tasks:
#             if task.deadline:
#                 deadlines.append(task.deadline)
