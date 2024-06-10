from celery import Celery
from celery.schedules import crontab
from src.config import settings

app = Celery("tasks", broker=settings.celery.BROKER_URL)


app.conf.beat_schedule = {
    "send_reminder_email_every_day": {
        "task": "src.celery_tasks.send_letter",
        "schedule": crontab(minute=0, hour=0),
    },
}
