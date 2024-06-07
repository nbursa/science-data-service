# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient
from app.config import settings

class MongoPipeline:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client["science-data-cluster"]

    def process_item(self, item, spider):
        self.db.articles.insert_one(dict(item))
        return item
