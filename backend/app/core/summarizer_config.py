from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field, field_validator

# Get the current directory and construct path to .env file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    """Application configuration settings"""

    # Database settings
    DATABASE_URL: str = Field(
        "",
        description="Main database connection string",
    )
    TEST_DATABASE_URL: str = Field(
        "",
        description="Test database connection string",
    )

    # Azure OpenAI settings
    AZURE_OPENAI_API_KEY: str = Field("", description="Azure OpenAI API key")
    AZURE_OPENAI_ENDPOINT: str = Field("", description="Azure OpenAI endpoint URL")
    AZURE_OPENAI_MODEL: str = Field("gpt4o-mini", description="Model deployment name")
    AZURE_OPENAI_API_VERSION: str = Field(
        "2024-08-01-preview", description="API version for Azure OpenAI"
    )

    # Application settings
    SUMMARY_LENGTH: int = Field(150, description="Desired summary length in words")
    DEFAULT_CATEGORY: str = Field("General", description="Default article category")
    APP_NAME: str = Field(
        "Personalized News Summarizer API", description="Application name"
    )
    APP_VERSION: str = Field("0.1.0", description="Application version")
    APP_PREFIX: str = Field("/api/v1", description="API route prefix")

    model_config = ConfigDict(
        env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore"
    )

    def __init__(self, **kwargs):
        if not ENV_FILE.exists():
            print(f"Warning: .env file not found at {ENV_FILE}")
            print("Please create .env file from .env.example")
        super().__init__(**kwargs)

    @field_validator("DATABASE_URL", "TEST_DATABASE_URL")
    def validate_db_url(cls, v: str) -> str:
        if not v.startswith("postgresql://"):
            raise ValueError("Database URL must be a PostgreSQL connection string")
        return v

    @field_validator("AZURE_OPENAI_ENDPOINT")
    def validate_endpoint(cls, v: str) -> str:
        if v and not v.startswith(("http://", "https://")):
            raise ValueError("Endpoint must be a valid HTTP(S) URL")
        return v


settings = Settings()
