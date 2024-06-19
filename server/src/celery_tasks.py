# import asyncio
# import logging
# from datetime import datetime, UTC, timedelta
# from sqlalchemy import select, and_
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import joinedload

# from src.database import async_session_maker
# from src.celeryconfig import app
# from src.tasks.models import Task
# from src.tasks_group.models import TasksGroup
# from src.users.models import User
# from src.util.email_util import email


# logger = logging.getLogger(__name__)


# async def get_tasks(session: AsyncSession) -> list[Task]:
#     close_deadline = datetime.now(UTC).date() + timedelta(days=3)
#     result = await session.execute(
#         select(Task)
#         .options(joinedload(Task.tasks_group).joinedload(TasksGroup.author))
#         .where(and_(Task.is_done == False, Task.deadline == close_deadline))
#     )
#     tasks = result.unique().scalars().all()
#     logger.debug(f"Prepared list of tasks with a close deadline: {tasks}")
#     return tasks


# async def get_users_from_task(session: AsyncSession) -> dict[User, list[Task]]:
#     try:
#         tasks = await get_tasks(session)
#         logger.debug(f"Have tasks: {tasks}")
#     except Exception as e:
#         logger.error(f"Have error from get tasks: {e}")
#     if tasks:
#         user_tasks = {}
#         for task in tasks:
#             if (
#                 task.tasks_group.author.is_active
#                 and task.tasks_group.author.is_verified
#             ):
#                 user_tasks.setdefault(task.tasks_group.author, [])
#                 user_tasks[task.tasks_group.author].append(task)
#         return user_tasks


# async def send_reminder_email() -> None:
#     async with async_session_maker() as session:
#         user_tasks = await get_users_from_task(session)
#         if user_tasks:
#             for user, tasks in user_tasks.items():
#                 tasks_list = "<br>".join(
#                     [
#                         f"Task: {task.title}  (from {task.tasks_group.title} group)"
#                         for task in tasks
#                     ]
#                 )
#                 try:
#                     await email.send_reminder_letter(user, tasks_list)
#                     logger.debug(f"Sent email to {user.email} for {tasks_list}")
#                 except Exception as e:
#                     logger.error(f"Failed to send email to {user.email}: {e}")


# @app.task
# def reminder_email() -> None:
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(send_reminder_email())
