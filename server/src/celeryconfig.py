from celery import Celery
from celery.schedules import crontab
from src.config import settings

app = Celery(
    "tasks", broker=settings.celery.BROKER_URL, backend=settings.celery.RESULT_BACKEND
)


app.conf.beat_schedule = {
    "send_reminder_email_every_day": {
        "task": "src.celery_tasks.reminder_email",
        "schedule": crontab(minute=0, hour=0),
    },
}
