import pytest
from unittest.mock import Mock
from backend.service.recommendation_service import RecommendationService

@pytest.fixture
def mock_db():
    db = Mock()
    course = Mock()
    course.code = "CS101"
    course.name = "Test Course"
    course.prerequisites = []
    course.description = None
    db.query.return_value.all.return_value = [course]
    return db

def test_recommendation_service(mock_db):
    service = RecommendationService(mock_db)
    
    # Mock Gemini response
    service.model = Mock()
    service.model.generate_content.return_value.text = "Test recommendation"
    
    result, metadata = service.generate_recommendation({
        "completed_courses": ["CS100"],
        "interests": "AI",
        "goals": "Research"
    })
    
    assert "Test recommendation" in result
    assert metadata["courses_considered"] == 1