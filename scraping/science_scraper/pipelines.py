from pymongo import MongoClient, errors
from app.config import settings
from scrapy.exceptions import DropItem


class MongoPipeline:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client["science-data-cluster"]

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == "natgeo_spider":
            collection_name = "natgeo-articles"
        else:
            collection_name = item.pop('category')

        collection = self.db[collection_name]

        existing_item = collection.find_one({'title': item['title']})

        if existing_item:
            spider.log(f"Duplicate item found: {item['title']}")
            raise DropItem(f"Duplicate item found: {item['title']}")
        else:
            try:
                collection.insert_one(dict(item))
                spider.log(f"Item added to MongoDB: {item['title']}")
            except errors.DuplicateKeyError:
                raise DropItem(f"Duplicate item found: {item['title']}")

        return item
