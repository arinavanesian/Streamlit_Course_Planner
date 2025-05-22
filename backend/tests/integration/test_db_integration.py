import pytest
from backend.data.database import Base, engine, SessionLocal
from backend.data.models import Course
from backend.data.repositories import CourseRepository

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def test_course_repository_integration():
    db = SessionLocal()
    repo = CourseRepository(db)
    
    course = repo.create({"code": "CS101", "name": "Test", "credits": 3, "type": "Core"})
    assert repo.get_by_code("CS101").name == "Test"
    
    with pytest.raises(Exception):
        repo.create({"code": "CS101", "name": "Duplicate"})
    
    db.close()