from celery import Celery
from app.config import settings

celery = Celery(
    'tasks',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Belgrade',
    enable_utc=True,
)

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'