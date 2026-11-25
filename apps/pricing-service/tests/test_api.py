from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "UP"}


def test_creates_a_quote() -> None:
    response = client.post("/quotes", json={"category": "economy", "days": 4})

    assert response.status_code == 200
    assert response.json() == {
        "category": "economy",
        "days": 4,
        "daily_rate": 40.0,
        "total": 160.0,
        "currency": "EUR",
    }


def test_rejects_an_unknown_category() -> None:
    response = client.post("/quotes", json={"category": "utility", "days": 1})

    assert response.status_code == 422
    assert "Unknown vehicle category" in response.json()["detail"]


def test_rejects_a_zero_day_quote() -> None:
    response = client.post("/quotes", json={"category": "economy", "days": 0})

    assert response.status_code == 422
