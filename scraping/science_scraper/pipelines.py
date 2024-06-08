from pymongo import MongoClient
from app.config import settings


class MongoPipeline:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client["science-data-cluster"]

    def process_item(self, item, spider):
        category = item.pop('category')
        self.db[category].insert_one(dict(item))
        return item
