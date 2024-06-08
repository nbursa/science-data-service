from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from app.config import settings

router = APIRouter()

client = MongoClient(settings.MONGODB_URI)
db = client["science-data-cluster"]


@router.get("/scraped-data-stats", response_model=dict)
def get_scraped_data_stats():
    try:
        stats = {
            "totalArticles": sum(db[collection].count_documents({}) for collection in db.list_collection_names()),
            "categories": {collection: db[collection].count_documents({}) for collection in db.list_collection_names()}
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
