from celery.schedules import crontab
from app.config import settings

broker_url = settings.CELERY_BROKER_URL
result_backend = settings.CELERY_RESULT_BACKEND

task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
timezone = 'Europe/Belgrade'
enable_utc = True

beat_schedule = {
    'run-spider-every-hour': {
        'task': 'scraping.celery_tasks.run_spider',
        'schedule': crontab(minute='0'),  # at the beginning of every hour
    },
    # 'translate-articles-every-hour': {
    #     'task': 'scraping.celery_tasks.translate_articles',
    #     'schedule': crontab(minute='0'),  # at the beginning of every hour
    # },
}
