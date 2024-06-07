import scrapy
from pymongo import MongoClient
from datetime import datetime

class ScienceSpider(scrapy.Spider):
    name = "science_spider"
    start_urls = ['https://www.sciencenews.org/']

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['science_data']
        self.collection = self.db['articles']

    def parse(self, response):
        for article in response.css('article'):
            item = {
                'title': article.css('h2 a::text').get(),
                'content': " ".join(article.css('div.entry-content p::text').getall()),
                'author': article.css('span.byline a::text').get(),
                'published_at': article.css('time::attr(datetime)').get(),
                'scraped_at': datetime.utcnow()
            }
            self.collection.insert_one(item)

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
