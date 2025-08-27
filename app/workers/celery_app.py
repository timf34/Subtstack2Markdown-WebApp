from celery import Celery
from ..settings import settings

celery_app = Celery(
    "substack",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(task_track_started=True)
