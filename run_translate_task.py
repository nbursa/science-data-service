from scraping.celery_tasks import translate_articles

if __name__ == "__main__":
    # Run the translate_articles task
    translate_articles.delay()
