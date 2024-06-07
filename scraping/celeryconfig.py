from celery.schedules import crontab

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
timezone = 'Europe/Belgrade'
enable_utc = True

beat_schedule = {
    'run-spider-every-minute': {
        'task': 'scraping.celery_tasks.run_spider',
        'schedule': crontab(minute='*/1'),  # every minute
    },
    'translate-articles-every-minute': {
        'task': 'scraping.celery_tasks.translate_articles',
        'schedule': crontab(minute='*/1'),  # every minute
    },
}
