from celery_tasks import run_spider, translate_articles

if __name__ == "__main__":
    run_spider.delay()
    translate_articles.delay()
