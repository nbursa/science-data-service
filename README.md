# Science Data Service

A content aggregation and social engagement platform focused on science articles.

## Features

- Automated web scraping of science news websites
- Article translation and summarization using OpenAI GPT API
- User authentication and commenting system
- Future forum for science discussions

## Getting Started

### Prerequisites

- Python 3.8+
- MongoDB
- Node.js



#### run uvicorn server
```bash
uvicorn app.main:app --reload
```

#### start celery worker
```bash
celery -A scraping.celery_tasks worker --loglevel=info
```

#### start celery beat
```bash
celery -A scraping.celery_tasks beat --loglevel=info
```

#### scrape articles
```bash
python -m scrapy crawl science_spider
```

