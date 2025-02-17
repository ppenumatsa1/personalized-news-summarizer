"""
News Article Summarization Service Module.

This module provides core business logic for article summarization, including
article creation, retrieval, and management functionality.
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.app.models.summarizer_models import Article
from backend.app.schemas.summarizer_schemas import (
    ArticleCreate,
    ArticleResponse,
    ArticleSummaryResponse,
)
from backend.app.exceptions.summarizer_exceptions import (  # Update import path
    ArticleNotFoundException,
    InvalidURLException,
    SummaryGenerationException,
    CategoryNotFoundException,
    ArticlesNotFoundForCategoryException,
)
from openai import AzureOpenAI
from app.logs.summarizer_logging import logger
from app.core.summarizer_config import settings
from newspaper import Article as NewspaperArticle
import json
from app.services.summarizer_service_helpers import (
    scrape_article,
    generate_summary_classify_article,
)


class SummarizerService:
    """
    Service class handling article summarization and management operations.

    Provides functionality for creating, retrieving, and managing article summaries
    while interfacing with the database and external APIs.
    """

    def __init__(self, db: Session, model=Article):
        """
        Initialize the summarizer service.

        Args:
            db (Session): SQLAlchemy database session
            model: Database model class (defaults to Article)
        """
        self.db = db
        self.model = model

    def summarize_article(self, url: str) -> ArticleSummaryResponse:
        """
        Generate a summary for an article from its URL.

        Args:
            url (str): URL of the article to summarize

        Returns:
            ArticleSummaryResponse: Contains title, summary, category, and content

        Raises:
            Exception: If article fetching or summarization fails
        """
        try:
            article_data = scrape_article(url)
            if not article_data["text"]:
                raise SummaryGenerationException("No content found in the article.")
            result = generate_summary_classify_article(article_data["text"])
            logger.info(f"Article summarized and classified successfully: {url}")
            return ArticleSummaryResponse(
                title=article_data["title"],
                url=url,
                summary=result["summary"],
                category=result["category"].lower(),  # Ensure category is lowercase
                content=article_data["text"],
            )
        except Exception as e:
            logger.error(f"Error summarizing article: {e}")
            raise SummaryGenerationException(str(e))

    def create_article(self, article_create: ArticleCreate) -> Article:
        """
        Create a new article entry with its summary.

        Args:
            article_create (ArticleCreate): Article creation data

        Returns:
            Article: Created article instance

        Raises:
            Exception: If article creation fails
        """
        try:
            existing_article = (
                self.db.query(self.model)
                .filter(self.model.url == article_create.url)
                .first()
            )
            if existing_article:
                logger.info(
                    f"Article with URL {article_create.url} already exists, returning existing article."
                )
                return existing_article

            if not article_create.url:
                raise InvalidURLException("URL cannot be empty")

            article_summary = self.summarize_article(article_create.url)
            article_data = article_create.model_dump()
            article_data.pop("summary", None)
            article_data.pop("category", None)
            article_data.pop("content", None)
            article_data.pop("title", None)

            new_article = self.model(
                **article_data,
                title=article_summary.title,
                summary=article_summary.summary,
                category=article_summary.category.lower(),
                content=article_summary.content,
            )
            self.db.add(new_article)
            self.db.commit()
            self.db.refresh(new_article)
            logger.info(f"Article created successfully: {new_article.id}")
            return new_article
        except Exception as e:
            logger.error(f"Failed to create article: {e}")
            raise SummaryGenerationException(str(e))

    def get_article(self, article_id: int) -> ArticleResponse:
        """
        Retrieve a single article by its ID.

        Args:
            article_id (int): ID of the article to retrieve

        Returns:
            ArticleResponse: Article data

        Raises:
            ArticleNotFoundException: If article doesn't exist
        """
        try:
            article = (
                self.db.query(self.model).filter(self.model.id == article_id).first()
            )
            if not article:
                raise ArticleNotFoundException(
                    f"Article with ID {article_id} not found"
                )
            logger.info(f"Article retrieved successfully: {article_id}")
            return article
        except ArticleNotFoundException as e:
            logger.error(f"Failed to retrieve article {article_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to retrieve article {article_id}: {e}")
            raise

    def get_articles_by_category(self, category_name: str) -> List[ArticleResponse]:
        """
        Retrieve all articles in a specific category.
        """
        try:
            articles = (
                self.db.query(self.model)
                .filter(self.model.category == category_name.lower())
                .all()
            )

            if not articles:
                logger.warning(f"No articles found for category: {category_name}")
                raise ArticlesNotFoundForCategoryException(category_name)

            logger.info(f"Found {len(articles)} articles for category: {category_name}")
            return articles

        except SQLAlchemyError as e:
            logger.error(
                f"Database error fetching articles for category {category_name}: {e}"
            )
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error fetching articles for category {category_name}: {e}"
            )
            raise ArticlesNotFoundForCategoryException(category_name) from e

    def get_articles(self) -> List[ArticleResponse]:
        """
        Retrieve all articles.

        Returns:
            List[ArticleResponse]: List of all articles

        Raises:
            Exception: If retrieval fails
        """
        try:
            articles = self.db.query(self.model).all()
            if not articles:
                logger.warning(f"Articles not found")
                return {"message": "Articles not found"}
            logger.info("Articles retrieved successfully")
            return articles
        except Exception as e:
            logger.error(f"Failed to retrieve articles: {e}")
            raise

    def delete_article(self, article_id: int):
        """
        Delete an article by its ID.

        Args:
            article_id (int): ID of the article to delete

        Raises:
            ArticleNotFoundException: If article doesn't exist
            Exception: If deletion fails
        """
        try:
            article = (
                self.db.query(self.model).filter(self.model.id == article_id).first()
            )
            if not article:
                raise ArticleNotFoundException(
                    f"Article with ID {article_id} not found"
                )
            self.db.delete(article)
            self.db.commit()
            logger.info(f"Article deleted successfully: {article_id}")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to delete article {article_id}: {e}")
            raise
