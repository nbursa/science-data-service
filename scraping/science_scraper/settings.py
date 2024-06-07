BOT_NAME = 'science_scraper'

SPIDER_MODULES = ['science_scraper.spiders']
NEWSPIDER_MODULE = 'science_scraper.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'science_scraper.pipelines.MongoPipeline': 300,
}
