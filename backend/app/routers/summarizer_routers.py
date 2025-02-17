"""
Article Summarizer API Router Module.

This module provides the routing logic for the article summarization API endpoints.
It handles article creation, retrieval, and deletion operations while managing
error handling and database interactions.
"""

from fastapi import APIRouter, Depends, HTTPException
from backend.app.logs.summarizer_logging import logger
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.app.schemas.summarizer_schemas import ArticleCreate, ArticleResponse
from backend.app.services.summarizer_services import SummarizerService
from backend.app.db.summarizer_db import get_db
from backend.app.exceptions.summarizer_exceptions import (
    ArticleNotFoundException,
    InvalidURLException,
    SummaryGenerationException,
    CategoryNotFoundException,
    ArticlesNotFoundForCategoryException,
)

router = APIRouter()


def get_summarizer_service(db: Session = Depends(get_db)) -> SummarizerService:
    """
    Dependency injection for the SummarizerService.

    Args:
        db (Session): Database session provided by FastAPI dependency system.

    Returns:
        SummarizerService: An instance of the summarizer service.
    """
    return SummarizerService(db)


@router.post("/articles/", response_model=ArticleResponse)
def create_article(article: ArticleCreate, service=Depends(get_summarizer_service)):
    """
    Create a new article from a URL.

    Args:
        article (ArticleCreate): Article creation data containing URL.
        service (SummarizerService): Injected summarizer service.

    Returns:
        ArticleResponse: Created article details.

    Raises:
        HTTPException: 503 if database unavailable
                      400 if validation fails
                      500 for unexpected errors
    """
    try:
        return service.create_article(article)
    except InvalidURLException as e:
        logger.error(f"Invalid URL error: {str(e)}")
        raise HTTPException(
            status_code=400, detail={"error": "InvalidURLException", "message": str(e)}
        )
    except SummaryGenerationException as e:
        logger.error(f"Summary generation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"error": "SummaryGenerationException", "message": str(e)},
        )
    except ArticleNotFoundException as e:
        logger.error(f"Application error: {str(e)}")
        raise HTTPException(
            status_code=400, detail={"error": e.__class__.__name__, "message": str(e)}
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error in create_article: {e}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "DatabaseError",
                "message": "Database service unavailable",
            },
        )
    except Exception as e:
        logger.error(f"Unexpected error in create_article: {e}")
        raise HTTPException(
            status_code=500, detail={"error": "InternalServerError", "message": str(e)}
        )


@router.get("/articles/", response_model=list[ArticleResponse])
def read_articles(service=Depends(get_summarizer_service)):
    """
    Retrieve all articles in the system.

    Args:
        service (SummarizerService): Injected summarizer service.

    Returns:
        List[ArticleResponse]: List of all articles.

    Raises:
        HTTPException: 503 if database unavailable
                      500 for unexpected errors
    """
    try:
        return service.get_articles()
    except SQLAlchemyError as e:
        logger.error(f"Database error in read_articles: {e}")
        raise HTTPException(
            status_code=503, detail="Unable to fetch articles from database"
        )
    except Exception as e:
        logger.error(f"Unexpected error in read_articles: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/articles/category/{category}", response_model=list[ArticleResponse])
def read_articles_by_category(category: str, service=Depends(get_summarizer_service)):
    """
    Retrieve articles filtered by category.
    """
    try:
        return service.get_articles_by_category(category)
    except (ArticlesNotFoundForCategoryException, CategoryNotFoundException) as e:
        # Handle both category-related exceptions
        logger.warning(f"Category error: {str(e)}")
        raise HTTPException(
            status_code=404, detail={"error": e.__class__.__name__, "message": str(e)}
        ) from None
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "DatabaseError",
                "message": f"Database error while fetching articles for category: {category}",
            },
        ) from None
    except Exception as e:
        logger.error(f"Unexpected error in read_articles_by_category: {str(e)}")
        # Re-raise as HTTP 500 if it's truly unexpected
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "An unexpected error occurred processing your request",
            },
        ) from None


@router.delete("/articles/{article_id}")
def delete_article(article_id: int, service=Depends(get_summarizer_service)):
    """
    Delete an article by its ID.

    Args:
        article_id (int): ID of the article to delete.
        service (SummarizerService): Injected summarizer service.

    Returns:
        dict: Success message if deletion successful.

    Raises:
        HTTPException: 503 if database unavailable
                      404 if article not found
                      500 for unexpected errors
    """
    try:
        service.delete_article(article_id)
        return {"message": "Article deleted successfully"}
    except ArticleNotFoundException as e:
        logger.error(f"Article not found: {str(e)}")
        raise HTTPException(
            status_code=404, detail={"error": e.__class__.__name__, "message": str(e)}
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error in delete_article: {e}")
        raise HTTPException(
            status_code=503, detail=f"Unable to delete article {article_id}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in delete_article: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
