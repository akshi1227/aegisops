from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_log():
    response = client.post(
        "/logs/",
        json={
            "timestamp": "2026-11-13T10:00:00",
            "log_level": "INFO",
            "message": "Clinical record verified securely",
            "status": "SUCCESS",
            "compliance_status": "COMPLIANT"
        }
    )
    assert response.status_code == 200
    assert response.json()["compliance_status"] == "COMPLIANT"

def test_read_logs():
    response = client.get("/logs/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)