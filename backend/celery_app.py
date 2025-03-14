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
    timezone="Asia/Ho_Chi_Minh",  # Set timezone to Vietnam
    enable_utc=False,  # Disable UTC to use the local timezone
    broker_connection_retry_on_startup=True,  # Ensure retry on startup
)

# Add periodic tasks
celery_app.conf.beat_schedule = {
    "check-and-generate-images": {
        "task": "backend.tasks.check_and_generate_images",
        "schedule": crontab(minute="*/1", hour=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23], day_of_week="*"),
    },
    # "check-and-generate-images-religion": {
    #     "task": "backend.tasks.check_and_generate_images_religion",
    #     "schedule": crontab(minute="*/1", hour=[12,13,14,15,16,17,18], day_of_week="*"),
    # },
    # "images-to-video-generation": {
    #     "task": "backend.tasks.images_to_video_generation",
    #     "schedule": crontab(minute="*/5", hour=[0], day_of_week="*"),
    # },
    "delete-oldest-images-tool-render": {
        "task": "backend.tasks.delete_oldest_images_tool_render",
        "schedule": crontab(hour=[1,2,3], minute="*/5", day_of_week="*"),
    },
    "delete-oldest-images-team-automation": {
        "task": "backend.tasks.delete_oldest_images_team_automation",
        "schedule": crontab(hour=[1,2,3], minute="*/5", day_of_week="*"),
    },
}

celery_app.autodiscover_tasks(["backend"])
