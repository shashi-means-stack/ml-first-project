from fastapi.testclient import TestClient

from first_ml_project.predict_api import app


def test_history_requires_auth_token() -> None:
    client = TestClient(app)

    unauthorized = client.get("/history")
    assert unauthorized.status_code == 200

    wrong_token = client.get("/history", headers={"Authorization": "Bearer wrong-token"})
    assert wrong_token.status_code == 401

    authorized_header = client.get("/history", headers={"Authorization": "Bearer demo-token"})
    assert authorized_header.status_code == 200

    authorized_query = client.get("/history?token=demo-token")
    assert authorized_query.status_code == 200
