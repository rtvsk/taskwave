from datetime import timedelta
from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379/0")

app.conf.beat_schedule = {
    "send_test_email_2min": {
        "task": "src.celery_tasks.send_test_email",
        "schedule": timedelta(minutes=2),
    },
}


# app.conf.beat_schedule = {
#     "check_deadlines_daily": {
#         "task": "celery_tasks.check_deadlines",
#         "schedule": timedelta(minutes=2),
#     },
# }
