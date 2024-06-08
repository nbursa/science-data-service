import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MONGODB_URI = os.getenv("MONGODB_URI")
    JWT_SECRET = os.getenv("JWT_SECRET")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")


settings = Settings()
