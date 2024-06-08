from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Article(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    content: str
    author: str
    translated_content: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
