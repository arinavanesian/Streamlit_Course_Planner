import pytest
from data.repositories import CourseRepository
from data.models import Course
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.database import Base
from sqlalchemy import inspect, Integer

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return Session()

def test_course_repository_add_course(db_session):
    repo = CourseRepository(db_session)
    course_data = {
        "code": "CS101",
        "name": "Intro to CS",
        "credits": 3,
        "type": "Core"
    }
    
    course = repo.create(course_data)
    assert course.id is not Integer
    assert db_session.query(Course).count() == 1

def test_get_by_code(db_session):
    repo = CourseRepository(db_session)
    db_session.add(Course(code="CS101", name="Test"))
    db_session.commit()
    
    assert repo.get_by_code("CS101").name == "Test"
    assert repo.get_by_code("INVALID") is None