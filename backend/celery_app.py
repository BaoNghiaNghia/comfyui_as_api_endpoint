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
    broker_connection_retry_on_startup=True,  # Ensure retry on startup
)

# Add periodic task to run every 5 minutes
celery_app.conf.beat_schedule = {
    "check-and-generate-images": {
        "task": "app.tasks.check_and_generate_images",
        "schedule": crontab(minute="*/1"),  # Every 5 minutes
    },
}
