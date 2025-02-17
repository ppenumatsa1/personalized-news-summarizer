import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock
from backend.app.services.summarizer_services import SummarizerService
from backend.app.db.summarizer_db import Base
from backend.app.models.summarizer_models import TestArticle
from backend.app.schemas.summarizer_schemas import ArticleCreate, ArticleSummaryResponse
from backend.app.exceptions.summarizer_exceptions import ArticleNotFoundException
from backend.app.core.summarizer_config import settings

DATABASE_URL = settings.TEST_DATABASE_URL  # Updated access pattern

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def summarizer_service(test_db):
    return SummarizerService(test_db, model=TestArticle)


@pytest.fixture(autouse=True)
def cleanup_database(test_db):
    yield
    test_db.query(TestArticle).delete()
    test_db.commit()


@pytest.fixture
def mock_scrape_article():
    with patch(
        "backend.app.services.summarizer_services.scrape_article"
    ) as mock:  # Changed path
        mock.return_value = {
            "title": "Test Article",
            "text": "This is a test article content.",
        }
        yield mock


@pytest.fixture
def mock_generate_summary():
    with patch(
        "backend.app.services.summarizer_services.generate_summary_classify_article"
    ) as mock:  # Changed path
        mock.return_value = {
            "summary": "This is a test summary",
            "category": "technology",
        }
        yield mock


def test_summarize_article_success(
    summarizer_service, mock_scrape_article, mock_generate_summary
):
    url = "https://example.com/test-article"

    mock_scrape_article.return_value = {
        "title": "Test Article",
        "text": "This is a test article content.",
    }
    mock_generate_summary.return_value = {
        "summary": "This is a test summary",
        "category": "technology",
    }

    response = summarizer_service.summarize_article(url)

    mock_scrape_article.assert_called_once_with(url)
    mock_generate_summary.assert_called_once_with("This is a test article content.")

    assert type(response).__name__ == "ArticleSummaryResponse"
    assert response.title == "Test Article"
    assert response.url == url
    assert response.summary == "This is a test summary"
    assert response.category == "technology"
    assert response.content == "This is a test article content."


def test_create_article_success(
    summarizer_service, mock_scrape_article, mock_generate_summary, test_db
):
    url = "https://example.com/test-article"
    article_create = ArticleCreate(url=url)

    new_article = summarizer_service.create_article(article_create)

    mock_scrape_article.assert_called_once_with(url)
    mock_generate_summary.assert_called_once()

    assert new_article.title == "Test Article"
    assert new_article.url == url
    assert new_article.summary == "This is a test summary"
    assert new_article.category == "technology"
    assert new_article.content == "This is a test article content."


def test_create_article_duplicate_url(
    summarizer_service, mock_scrape_article, mock_generate_summary, test_db
):
    url = "https://example.com/test-article"
    article_create = ArticleCreate(url=url)

    # Create first article
    first_article = summarizer_service.create_article(article_create)

    # Reset mock call counts
    mock_scrape_article.reset_mock()
    mock_generate_summary.reset_mock()

    # Try to create article with same URL
    second_article = summarizer_service.create_article(article_create)

    # Verify mocks weren't called for the second attempt
    mock_scrape_article.assert_not_called()
    mock_generate_summary.assert_not_called()

    assert second_article.id == first_article.id
    assert second_article.url == first_article.url


def test_get_article_success(
    summarizer_service, mock_scrape_article, mock_generate_summary, test_db
):
    article_create = ArticleCreate(url="https://example.com/test-article")
    article = summarizer_service.create_article(article_create)

    response = summarizer_service.get_article(article.id)
    assert response.id == article.id


def test_get_articles_by_category_success(
    summarizer_service, mock_scrape_article, mock_generate_summary, test_db
):
    article_create = ArticleCreate(url="https://example.com/test-article")
    summarizer_service.create_article(article_create)

    response = summarizer_service.get_articles_by_category("technology")
    assert len(response) == 1
    assert response[0].category == "technology"


def test_get_articles_success(
    summarizer_service, mock_scrape_article, mock_generate_summary, test_db
):
    # Clean up any existing data
    test_db.query(TestArticle).delete()
    test_db.commit()

    article_create = ArticleCreate(url="https://example.com/test-article")
    summarizer_service.create_article(article_create)

    response = summarizer_service.get_articles()
    assert len(response) == 1
    assert response[0].title == "Test Article"
    assert response[0].summary == "This is a test summary"
    assert response[0].category == "technology"


def test_delete_article_success(
    summarizer_service, mock_scrape_article, mock_generate_summary, test_db
):
    article_create = ArticleCreate(url="https://example.com/test-article")
    article = summarizer_service.create_article(article_create)

    summarizer_service.delete_article(article.id)
    assert test_db.query(TestArticle).filter_by(id=article.id).first() is None
