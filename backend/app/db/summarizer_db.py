from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.summarizer_config import settings
from app.logs.summarizer_logging import logger

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL  # Updated access pattern

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        logger.info("Database session created")
        yield db
    finally:
        db.close()
        logger.info("Database session closed")
