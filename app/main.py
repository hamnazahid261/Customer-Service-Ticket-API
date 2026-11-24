
import logging

from fastapi import FastAPI, HTTPException

from app import models
from app.database import Base, engine
from app.routers import tickets, users, auth


# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# Initialize FastAPI application
app = FastAPI(
    title="Customer Service Ticket API",
    description="Backend API for managing customer service tickets",
    version="1.0.0"
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Register API routers
app.include_router(tickets.router)
app.include_router(users.router)
app.include_router(auth.router)


logger.info("Customer Service Ticket API initialized successfully")


# Home endpoint
@app.get("/")
def home():
    logger.info("Home endpoint accessed")

    return {
        "message": "Customer Service Ticket API is running"
    }


# Database connection test endpoint
@app.get("/test-db")
def test_database():
    try:
        with engine.connect():
            pass

        logger.info("PostgreSQL connection successful")

        return {
            "message": "PostgreSQL connected successfully!"
        }

    except Exception as e:
        logger.exception("PostgreSQL connection failed")

        raise HTTPException(
            status_code=503,
            detail="Database connection failed. Please try again later."
        ) from e
