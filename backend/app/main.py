from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import summarizer_routers
from backend.app.core.summarizer_config import settings
from backend.app.logs.summarizer_logging import logger
from backend.app.db.summarizer_db import Base, engine


app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's default port
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables created successfully")

app.include_router(
    summarizer_routers.router, prefix=settings.APP_PREFIX, tags=["Summarizer API"]
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Personalized News Summarizer API"}
