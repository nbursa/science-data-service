from fastapi import FastAPI
from pymongo import MongoClient
from app.config import settings
from app.routers import articles, auth, comments

app = FastAPI()

# Create the MongoClient instance
client = MongoClient(settings.MONGODB_URI)

# Select the database
db = client["science-data-cluster"]

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(articles.router, prefix="/articles", tags=["articles"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])

@app.get("/test-db-connection")
def test_db_connection():
    try:
        # Check the connection by running a simple command
        db.command("ping")
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"error": str(e)}