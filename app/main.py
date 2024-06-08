from fastapi import FastAPI
from pymongo import MongoClient
from app.config import settings
from app.routers import articles, auth, comments, statistics
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient(settings.MONGODB_URI)

db = client["science-data-cluster"]

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(articles.router, prefix="/api/articles", tags=["articles"])
app.include_router(comments.router, prefix="/api/comments", tags=["comments"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["statistics"])


@app.get("/test-db-connection")
def test_db_connection():
    try:
        # Check the connection by running a simple command
        db.command("ping")
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"error": str(e)}
