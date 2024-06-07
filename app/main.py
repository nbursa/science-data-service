from fastapi import FastAPI
from mongoengine import connect
from app.config import settings
from app.routers import articles, auth, comments

app = FastAPI()

connect(db=settings.MONGODB_URI)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(articles.router, prefix="/articles", tags=["articles"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
