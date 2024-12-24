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
        # "schedule": crontab(minute="*/2", hour="20-23,0-5"),  # Every 2 minutes from 8 PM to 6 AM
        "schedule": crontab(minute="*/1"),  # Every 1 minutes
    },
    "delete-oldest-images-tool-render": {
        "task": "backend.tasks.delete_oldest_images_tool_render",
        # "schedule": crontab(hour=1, minute="*/5", day_of_week="*"),  # Every 5 minutes between 1:00 AM and 2:00 AM
        "schedule": crontab(minute="*/2"),  # Every 2 minutes
    },
    "delete-oldest-images-team-automation": {
        "task": "backend.tasks.delete_oldest_images_team_automation",
        # "schedule": crontab(hour=1, minute="*/5", day_of_week="*"),  # Every 5 minutes between 1:00 AM and 2:00 AM
        "schedule": crontab(minute="*/3"),  # Every 2 minutes
    },
}

celery_app.autodiscover_tasks(["backend"])