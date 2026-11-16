from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_backtest_returns_results():
    response = client.get("/backtest/AAPL")
    assert response.status_code == 200

    data = response.json()
    assert data["ticker"] == "AAPL"
    assert data["days"] == 20
    for side in ["strategy", "buy_and_hold"]:
        assert data[side]["final_value"] > 0
        assert data[side]["max_drawdown"] <= 0


def test_lowercase_ticker_works():
    response = client.get("/backtest/aapl")
    assert response.status_code == 200
    assert response.json()["ticker"] == "AAPL"


def test_custom_days():
    response = client.get("/backtest/KO?days=50")
    assert response.status_code == 200
    assert response.json()["days"] == 50


def test_unknown_ticker_returns_404():
    response = client.get("/backtest/ZZZZ")
    assert response.status_code == 404


def test_invalid_days_returns_422():
    response = client.get("/backtest/AAPL?days=abc")
    assert response.status_code == 422
