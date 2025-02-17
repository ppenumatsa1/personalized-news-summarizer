from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class ArticleBase(BaseModel):
    title: Optional[str] = None
    url: str
    content: Optional[str] = None
    summary: Optional[str] = None
    category: Optional[str] = None


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ArticleResponse(BaseModel):
    id: int
    title: Optional[str] = None
    url: str
    summary: Optional[str] = None
    category: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class ArticleSummaryResponse(BaseModel):
    title: Optional[str] = None
    url: str
    content: Optional[str] = None
    summary: Optional[str] = None
    category: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
