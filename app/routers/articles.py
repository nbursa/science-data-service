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

class ArticleModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    title: str
    content: str
    author: str
    published_at: Optional[str] = None

def get_collection(category: str) -> Collection:
    if category not in db.list_collection_names():
        raise HTTPException(status_code=404, detail="Category not found")
    return db[category]

@router.get("/{category}", response_description="List all articles in a category", response_model=List[ArticleModel])
def list_articles(category: str):
    try:
        collection = get_collection(category)
        articles = list(collection.find({}))
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{category}/{article_id}", response_description="Get a single article by ID", response_model=ArticleModel)
def get_article(category: str, article_id: str):
    try:
        collection = get_collection(category)
        article = collection.find_one({"_id": ObjectId(article_id)})
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")
        return article
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{category}", response_description="Add new article", response_model=ArticleModel)
def add_article(category: str, article: ArticleModel):
    try:
        collection = get_collection(category)
        result = collection.insert_one(article.dict(by_alias=True))
        article.id = str(result.inserted_id)
        return article
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{category}/{article_id}", response_description="Update an article", response_model=ArticleModel)
def update_article(category: str, article_id: str, article: ArticleModel):
    try:
        collection = get_collection(category)
        update_data = article.dict(by_alias=True)
        result = collection.update_one({"_id": ObjectId(article_id)}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Article not found")
        return article
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{category}/{article_id}", response_description="Delete an article")
def delete_article(category: str, article_id: str):
    try:
        collection = get_collection(category)
        result = collection.delete_one({"_id": ObjectId(article_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Article not found")
        return {"deleted_count": result.deleted_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
