import requests
import os
import time

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

def test_full_recommendation_flow():
    test_course = {
        "code": "TEST101",
        "name": "Test Course",
        "credits": 3,
        "type": "Core"
    }
    
    response = requests.post(f"{API_URL}/courses", json=test_course)
    assert response.status_code == 200
    
    rec_response = requests.post(
        f"{API_URL}/recommendations",
        json={
            "completed_courses": ["TEST101"],
            "interests": "Testing",
            "goals": "Quality Assurance"
        }
    )
    
    assert rec_response.status_code == 200
    assert "TEST101" in rec_response.json()["recommendation"]