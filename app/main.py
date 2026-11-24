from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routers import tickets, users, auth

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


@app.get("/")
def home():
    return {
        "message": "Customer Service Ticket API is running"
    }


@app.get("/test-db")
def test_database():
    try:
        connection = engine.connect()
        connection.close()

        return {
            "message": "PostgreSQL connected successfully!"
        }

    except Exception as e:
        return {
            "error": str(e)
        }