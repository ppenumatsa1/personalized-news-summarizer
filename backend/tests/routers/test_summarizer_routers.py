import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.app.main import app
from backend.app.routers.summarizer_routers import get_summarizer_service
from backend.app.schemas.summarizer_schemas import ArticleCreate, ArticleResponse
from backend.app.db.summarizer_db import get_db
from backend.app.core.summarizer_config import settings

client = TestClient(app)
API_PREFIX = settings.APP_PREFIX  # Updated access pattern


class MockSummarizerService:
    def __init__(self, db: Session):
        self.db = db

    def create_article(self, article: ArticleCreate) -> ArticleResponse:
        return ArticleResponse(
            id=1,
            title=article.title,
            summary=article.summary,
            category=article.category,
            url="https://example.com/test",
        )

    def get_articles(self) -> list:
        return [
            ArticleResponse(
                id=1,
                title="Test",
                summary="Test summary",
                category="Test",
                url="https://example.com/test",
            )
        ]

    def get_articles_by_category(self, category_name: str) -> list:
        return [
            ArticleResponse(
                id=1,
                title="Test",
                summary="Test summary",
                category=category_name,
                url="https://example.com/test",
            )
        ]

    def delete_article(self, article_id: int):
        pass


@pytest.fixture
def mock_service():
    return MockSummarizerService(None)


@pytest.fixture
def override_get_summarizer_service(mock_service):
    def _override_get_summarizer_service():
        return mock_service

    app.dependency_overrides[get_summarizer_service] = _override_get_summarizer_service
    yield
    app.dependency_overrides.clear()


# Test functions with updated assertions
def test_create_article(override_get_summarizer_service):
    response = client.post(
        f"{API_PREFIX}/articles/",
        json={
            "title": "Test",
            "summary": "Test summary",
            "category": "Test",
            "url": "https://example.com/test",  # Add url field to match schema
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Test",
        "summary": "Test summary",
        "category": "Test",
        "url": "https://example.com/test",
    }


def test_read_articles(override_get_summarizer_service):
    response = client.get(f"{API_PREFIX}/articles/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Test",
            "summary": "Test summary",
            "category": "Test",
            "url": "https://example.com/test",
        }
    ]


def test_read_articles_by_category(override_get_summarizer_service):
    response = client.get(f"{API_PREFIX}/articles/category/Test")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Test",
            "summary": "Test summary",
            "category": "Test",
            "url": "https://example.com/test",
        }
    ]


def test_remove_article(override_get_summarizer_service):
    response = client.delete(f"{API_PREFIX}/articles/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Article deleted successfully"}
