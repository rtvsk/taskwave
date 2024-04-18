from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

# from datetime import date
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from src.celeryconfig import app
from src.users.models import User
from src.util.email_util import Email

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
sync_engine = create_engine(DATABASE_URL, echo=True)
sync_session_maker = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
)


# CHECK SESSION AND CHECK 'send_test'
@app.task
def send_test_email():
    with sync_session_maker() as session:
        result = session.execute(select(User).where(User.login == "Lera"))  # FOR TEST

        user = result.fetchone()
        print(user)
        print("before")
    try:
        Email.send_test(user[0])
    except Exception as e:
        print(f"Something wrooooooong: {e}")
