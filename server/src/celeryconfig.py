from celery import Celery
from celery.schedules import crontab

app = Celery("tasks", broker="redis://localhost:6379/0")


app.conf.beat_schedule = {
    "send_reminder_email_every_day": {
        "task": "src.celery_tasks.send_letter",
        "schedule": crontab(minute=0, hour=0),
    },
}
