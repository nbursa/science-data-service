from fastapi import APIRouter, HTTPException, Depends
from pymongo.collection import Collection
from pymongo import MongoClient
from app.config import settings
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

router = APIRouter()

# Create the MongoClient instance
client = MongoClient(settings.MONGODB_URI)
db = client["science-data-cluster"]
articles_collection: Collection = db["articles"]

class ArticleModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    title: str
    content: str
    author: str
    published_at: Optional[str] = None

@router.get("/", response_description="List all articles", response_model=List[ArticleModel])
def list_articles():
    try:
        articles = list(articles_collection.find({}))
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{article_id}", response_description="Get a single article by ID", response_model=ArticleModel)
def get_article(article_id: str):
    try:
        article = articles_collection.find_one({"_id": ObjectId(article_id)})
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")
        return article
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_description="Add new article", response_model=ArticleModel)
def add_article(article: ArticleModel):
    try:
        result = articles_collection.insert_one(article.dict(by_alias=True))
        article.id = str(result.inserted_id)
        return article
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{article_id}", response_description="Update an article", response_model=ArticleModel)
def update_article(article_id: str, article: ArticleModel):
    try:
        update_data = article.dict(by_alias=True)
        result = articles_collection.update_one({"_id": ObjectId(article_id)}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Article not found")
        return article
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{article_id}", response_description="Delete an article")
def delete_article(article_id: str):
    try:
        result = articles_collection.delete_one({"_id": ObjectId(article_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Article not found")
        return {"deleted_count": result.deleted_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
