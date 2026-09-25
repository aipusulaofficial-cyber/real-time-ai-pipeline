from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis import strategies as st

from service import app

client = TestClient(app)


def test_contract() -> None:
    assert client.get("/health/live").status_code == 200


@given(st.text(min_size=1, max_size=32))
def test_property(value: str) -> None:
    if not value.strip():
        return
    response = client.post(
        "/v1/stream",
        json={
            "key": value,
            "payload": {"value": 1, "timestamp": 1},
        },
    )
    assert response.status_code == 200, response.text
