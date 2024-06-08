import logging
from fastapi import APIRouter, HTTPException, Depends, Query
from pymongo.collection import Collection
from pymongo import MongoClient
from app.config import settings
from bson import ObjectId
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MongoClient instance
client = MongoClient(settings.MONGODB_URI)
db = client["science-data-cluster"]


class ArticleModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    title: str = "Untitled"
    content: str = "No content available."
    author: str = "Unknown author"
    published_at: Optional[str] = None
    image_urls: List[str] = []

    @field_validator("title", mode="before")
    def set_title(cls, v):
        return v or "Untitled"

    @field_validator("content", mode="before")
    def set_content(cls, v):
        return v or "No content available."

    @field_validator("author", mode="before")
    def set_author(cls, v):
        return v or "Unknown author"

    @classmethod
    def from_mongo(cls, document):
        if document:
            document["_id"] = str(document["_id"])
        return cls(**document)


def get_collection(category: str) -> Collection:
    if category not in db.list_collection_names():
        raise HTTPException(status_code=404, detail="Category not found")
    return db[category]


@router.get("/{category}", response_description="List all articles in a category", response_model=List[ArticleModel])
def list_articles(category: str, skip: int = Query(0), limit: int = Query(4)):
    try:
        collection = get_collection(category)
        logger.info(f"Fetching articles for category {category}, skip: {skip}, limit: {limit}")
        articles = [ArticleModel.from_mongo(article) for article in collection.find({}).skip(skip).limit(limit)]
        logger.info(f"Returning articles for category {category}: {articles}")
        return articles
    except Exception as e:
        logger.error(f"Error fetching articles for category {category}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{category}/{article_id}", response_description="Get a single article by ID", response_model=ArticleModel)
def get_article(category: str, article_id: str):
    try:
        collection = get_collection(category)
        article = collection.find_one({"_id": ObjectId(article_id)})
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")
        return ArticleModel.from_mongo(article)
    except Exception as e:
        logger.error(f"Error fetching article {article_id} for category {category}: {str(e)}")
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
