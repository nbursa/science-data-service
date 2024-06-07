import scrapy
from science_scraper.items import ArticleItem

class ScienceSpider(scrapy.Spider):
    name = "science_spider"
    start_urls = ['https://www.sciencenews.org/']

    def parse(self, response):
        for article in response.css('article'):
            item = ArticleItem()
            item['title'] = article.css('h2 a::text').get()
            item['content'] = " ".join(article.css('div.entry-content p::text').getall())
            item['author'] = article.css('span.byline a::text').get()
            item['published_at'] = article.css('time::attr(datetime)').get()
            yield item

#             translated_article = translate_article.apply_async(args=[item], queue='translation')
#             yield translated_article.get()

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
