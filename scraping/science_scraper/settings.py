BOT_NAME = 'science_scraper'

SPIDER_MODULES = ['scraping.science_scraper.spiders']
NEWSPIDER_MODULE = 'scraping.science_scraper.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'scraping.science_scraper.pipelines.MongoPipeline': 300,
}
