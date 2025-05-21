from fastapi.testclient import TestClient
from main import app
import os

client = TestClient(app)

def test_list_courses():
    response = client.get("/api/v1/courses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_recommendations():
    test_data = {
        "completed_courses": ["CS111"],
        "interests": "AI",
        "goals": "Research"
    }
    response = client.post("/api/v1/recommendations", json=test_data)
    
    assert response.status_code == 200
    assert "recommendation" in response.json()
    assert "metadata" in response.json()