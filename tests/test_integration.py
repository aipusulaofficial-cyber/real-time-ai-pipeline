from fastapi.testclient import TestClient

from service import app


def test_http_contract_and_domain() -> None:
    client = TestClient(app)
    assert client.get("/health/live").status_code == 200
    response = client.post(
        "/v1/stream",
        json={
            "key": "integration",
            "payload": {
                "samples": [
                    {"key": "integration", "value": 1, "timestamp": 1},
                    {"key": "integration", "value": 3, "timestamp": 2},
                ]
            },
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["window_value"] == 2.0
