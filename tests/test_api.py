
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Customer Service Ticket API is running"
    }


def test_openapi_schema():
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Customer Service Ticket API"


def test_swagger_documentation():
    response = client.get("/docs")

    assert response.status_code == 200


def test_database_connection():
    response = client.get("/test-db")

    assert response.status_code == 200
    assert response.json() == {
        "message": "PostgreSQL connected successfully!"
    }
