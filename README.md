# Science Data Service - A Science News Aggregator

⚠️ Work in progress. 

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
- Docker (optional but recommended for easy setup)

### Setup

#### Clone the repository
```bash
git clone https://github.com/nbursa/science-data-service.git
cd science-data-service
```

#### Install dependencies
```bash
pip install -r requirements.txt
```

#### Start services with Docker Compose (optional)
If you prefer to use Docker, you can start MongoDB and Redis using Docker Compose:

```bash
docker-compose up -d
```

### Running the Application

#### Run the Uvicorn server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Start Celery worker
```bash
celery -A scraping.celery_tasks worker --loglevel=info
```

#### Start Celery beat
```bash
celery -A scraping.celery_tasks beat --loglevel=info
```

#### Scrape articles
```bash
python -m scrapy crawl <spider_name>
```

## Usage

### Accessing the Application
After starting the Uvicorn server, you can access the application at:
```
http://localhost:8000
```

### API Documentation
API documentation is available at:
```
http://localhost:8000/docs
```

### Environment Variables
Make sure to set the necessary environment variables for connecting to MongoDB and Redis, as well as for the OpenAI API key for article translation and summarization.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
