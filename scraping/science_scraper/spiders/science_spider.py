import scrapy
from ..items import ArticleItem

class ScienceSpider(scrapy.Spider):
    name = "science_spider"
    start_urls = [
        'https://www.sciencenews.org/topic/health-medicine',
        'https://www.sciencenews.org/topic/humans',
        'https://www.sciencenews.org/topic/life',
        'https://www.sciencenews.org/topic/earth',
        'https://www.sciencenews.org/topic/physics',
        'https://www.sciencenews.org/topic/space'
    ]
    article_counts = {}

    def parse(self, response):
        category = response.url.split('/')[-1]  # Extract the category from the URL
        if category not in self.article_counts:
            self.article_counts[category] = 0

        self.log(f"Scraping category: {category}")
        article_selectors = response.css(
            'h3[class^="compact-feature-primary__title"] a::attr(href), '
            'h3[class^="compact-feature-secondary__title"] a::attr(href), '
            'h3[class^="post-item-river__title"] a::attr(href)'
        )

        if not article_selectors:
            self.log(f"No articles found on category page: {response.url}")

        for article_link in article_selectors:
            if self.article_counts[category] >= 10:
                break  # Stop processing after 10 articles

            article_url = article_link.get()
            if article_url:
                self.article_counts[category] += 1
                yield response.follow(article_url, self.parse_article, meta={'category': category})

        # Follow the pagination link only if the limit is not reached
        if self.article_counts[category] < 10:
            next_page = response.css('a.next::attr(href)').get()
            if next_page:
                self.log(f"Following pagination link for category {category}: {next_page}")
                yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        category = response.meta['category']
        self.log(f"Scraping article in category: {category} from URL: {response.url}")

        item = ArticleItem()
        item['title'] = response.css('h1[class^="header-default__title"]::text').get()
        if item['title']:
            item['title'] = item['title'].strip()
        else:
            self.log(f"Missing title on page: {response.url}")

        content = response.css('div[class^="single__body"] div[class^="single__content"] p::text, div[class^="single__body"] div[class^="single__content"] p a::text').getall()
        if content:
            item['content'] = " ".join(content).strip()
        else:
            self.log(f"Missing content on page: {response.url}")

        author = response.css('p[class^="byline__authors"] a[class^="byline-link"]::text').get()
        if author:
            item['author'] = author.strip()
        else:
            item['author'] = None
            self.log(f"Missing author on page: {response.url}")

        published_at = response.css('p[class^="byline__published"] time::attr(datetime)').get()
        if published_at:
            item['published_at'] = published_at.strip()
        else:
            item['published_at'] = None
            self.log(f"Missing published_at on page: {response.url}")

        item['image_urls'] = response.css('figure img::attr(src)').getall()  # Get all image URLs
        if not item['image_urls']:
            self.log(f"Missing image URLs on page: {response.url}")

        item['category'] = category  # Add the category to the item

        yield item
