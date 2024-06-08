import logging
from celery import Celery
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from app.services.translation import translate_content
from app.config import settings
from pymongo import MongoClient

from scraping.science_scraper.spiders.science_spider import ScienceSpider

app = Celery('tasks', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = MongoClient(settings.MONGODB_URI)
db = client["science-data-cluster"]
articles_collection = db["articles"]


@app.task
def run_spider():
    logger.info("Running Spider Task")
    process = CrawlerProcess(get_project_settings())
    process.crawl(ScienceSpider)
    process.start()


# @app.task
# def translate_articles():
#     logger.info("Running Translate Articles Task")
#     articles = articles_collection.find({"translated_content": {"$exists": False}})
#     for article in articles:
#         translated_content = translate_content(article["content"])
#         if translated_content:
#             articles_collection.update_one(
#                 {"_id": article["_id"]},
#                 {"$set": {"translated_content": translated_content}}
#             )
#             logger.info(f"Translated article ID: {article['_id']}")
#         else:
#             logger.error(f"Failed to translate article ID: {article['_id']}")
