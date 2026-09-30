import os
os.environ["DEMO_MODE"] = "true"
os.environ["GEMINI_API_KEY"] = ""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "FitBuddy" in response.text


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_demo_plan():
    response = client.post("/generate-workout", data={
        "name": "Alex", "user_id": "test001", "age": 20, "weight": 65,
        "goal": "general wellness", "intensity": "medium",
    })
    assert response.status_code == 200
    assert "7-Day Workout Plan" in response.text or "Workout Plan" in response.text
    assert "Day 1" in response.text


def test_feedback_update():
    response = client.post("/submit-feedback", data={"user_id": "test001", "feedback": "Add more mobility."})
    assert response.status_code == 200
    assert "updated" in response.text.lower()
