# file: tests/test_main.py
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_root_returns_message_and_version():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "hello devops"
    assert "version" in response.json()

def test_health_is_ok():
    # Load balancer và Kubernetes dựa vào endpoint này để quyết định có gửi traffic vào hay không.
    assert client.get("/health").json() == {"status": "ok"}

def test_fail_returns_500():
    assert client.get("/fail").status_code == 500

def test_metrics_count_requests_by_status():
    # Alert ở giai đoạn 8 dựa trên metric này, nên label status phải đúng.
    client.get("/")
    client.get("/fail")
    body = client.get("/metrics").text
    assert 'http_requests_total{path="/",status="200"}' in body
    assert 'http_requests_total{path="/fail",status="500"}' in body
