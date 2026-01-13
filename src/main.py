import logging
import os 
from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.config import get_settings
from src.db.factory import make_database

# Week 1: No complex middleware or API key authentication
from src.routes import ask, ping, papers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Week1: Simplified lifespan for learning purposes.
    """
    logger.info("Starting up the RAG service...")
    settings = get_settings()
    app.state.settings = settings
    database = make_database()
    app.state.database = database
    logger.info("Database connected.")

    # Placeholder for future services (e.g., PDF parser)
    app.state.pdf_parser_service = None
    app.state.opensearch_service = None
    app.state.llm_service = None

    logger.info("API services ready.")
    yield


    # Cleanup 
    database.teardown()
    logger.info("RAG service shut down.")

app = FastAPI(
    title="RAG Service",
    version="0.1.0",
    description="A simple RAG service for learning purposes.",
    root_path = "/api/v1",
    lifespan=lifespan,
)

# Include routes
app.include_router(ping.router)
app.include_router(ask.router)
app.include_router(papers.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)