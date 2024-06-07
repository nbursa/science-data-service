from celery import Celery
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from science_scraper.spiders.science_spider import ScienceSpider
from app.services.translation import translate_content
from app.models.article import Article
from scraping.science_scraper.spiders.science_spider import ScienceSpider

app = Celery('tasks', broker='redis://localhost:6379/0')

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
