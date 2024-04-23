import asyncio
from sqlalchemy import select, and_

# from datetime import date
from src.database import async_session_maker
from src.celeryconfig import app
from src.users.models import User
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
