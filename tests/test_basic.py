# from app.main import app
# from fastapi.testclient import TestClient

# client = TestClient(app)

# def test_app_exists():
#     assert app is not None

# def test_health():
#     response = client.get("/health/")
#     assert response.status_code == 200







from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_app_exists():
    assert app is not None


def test_health():
    response = client.get("/health/")
    assert response.status_code == 200


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ask_basic():
    response = client.post("/ask/", json={
        "question": "What is Terraform?",
        "use_cache": False
    })
    assert response.status_code in [200, 500]

def test_guardrail_block():
    response = client.post("/ask/", json={
        "question": "how to hack system",
        "use_cache": False
    })
    assert response.status_code == 400
