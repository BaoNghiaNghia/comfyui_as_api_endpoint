from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "backend",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True,  # Ensure retry on startup
)

# Add periodic tasks
celery_app.conf.beat_schedule = {
    "check-and-generate-images": {
        "task": "backend.tasks.check_and_generate_images",
        "schedule": crontab(minute="*/1"),  # Every 5 minutes
    },
    "delete-oldest-images": {
        "task": "backend.tasks.delete_oldest_images",
        "schedule": crontab(hour=1, minute=0),  # Every day at 1:00 AM
    },
}

celery_app.autodiscover_tasks(["backend"])