import scrapy
from ..items import NatGeoItem


class NatGeoSpider(scrapy.Spider):
    name = "natgeo_spider"
    start_urls = [
        'https://www.nationalgeographic.com/science'
    ]

    def parse(self, response):
        # Select all articles on the page
        article_selectors = response.css('a[href*="/science/article/"]::attr(href)')

        for article_link in article_selectors:
            article_url = response.urljoin(article_link.get())
            yield response.follow(article_url, self.parse_article)

        # Follow pagination links if available
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        self.log(f"Scraping article from URL: {response.url}")

        item = NatGeoItem()

        title = response.css('[data-testid="prism-headline"] h1::text').get()
        if title:
            item['title'] = title.strip()
        else:
            self.log(f"Missing title on page: {response.url}")
            item['title'] = 'No title found'

        description = response.css('[data-testid="prism-headline"] p span::text').get()
        if description:
            item['description'] = description.strip()
        else:
            self.log(f"Missing description on page: {response.url}")
            item['description'] = 'No description found'

        content = response.css('[data-testid="prism-GridRow"]').get()
        if content:
            item['content'] = content.strip()
        else:
            self.log(f"Missing content on page: {response.url}")
            item['content'] = 'No content found'

        image_url = response.css('[data-testid="prism-image"] img::attr(src)').get()
        if image_url:
            item['image_urls'] = [image_url.strip()]
        else:
            self.log(f"Missing image URL on page: {response.url}")
            item['image_urls'] = []

        author = response.css('span[data-testid="byline-name"]::text').get()
        if author:
            item['author'] = author.strip()
        else:
            self.log(f"Missing author on page: {response.url}")
            item['author'] = 'No author found'

        published_at = response.css('time::attr(datetime)').get()
        if published_at:
            item['published_at'] = published_at.strip()
        else:
            self.log(f"Missing published_at on page: {response.url}")
            item['published_at'] = 'No publication date found'

        item['category'] = response.url.split('/')[4]

        yield item
