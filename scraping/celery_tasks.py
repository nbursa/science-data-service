import logging
from celery import Celery
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from app.services.translation import translate_content
from app.models.article import Article
from scraping.science_scraper.spiders.science_spider import ScienceSpider
from app.config import settings

app = Celery('tasks', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Belgrade',
    enable_utc=True,
)

@app.task
def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(ScienceSpider)
    process.start()

@app.task
def translate_articles():
    articles = Article.objects(translated_content=None)
    for article in articles:
        translated_content = translate_content(article.content)
        article.translated_content = translated_content
        article.save()
