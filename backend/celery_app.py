from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Add periodic task to run at 2 AM daily
celery_app.conf.beat_schedule = {
    "check-and-generate-images": {
        "task": "app.tasks.check_and_generate_images",
        "schedule": crontab(hour=2, minute=0),  # 2 AM UTC
    },
}
