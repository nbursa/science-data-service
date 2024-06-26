import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    published_at = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()


class NatGeoItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    description = scrapy.Field()
    author = scrapy.Field()
    published_at = scrapy.Field()
    image_urls = scrapy.Field()