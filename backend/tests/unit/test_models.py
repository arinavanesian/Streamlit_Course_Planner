import pytest
from backend.data.models import Course, Prerequisite
from sqlalchemy import inspect

def test_course_model():
    course = Course(
        code="CS101",
        name="Intro to CS",
        credits=3,
        type="Core",
        description="Basic CS concepts"
    )
    
    assert course.code == "CS101"
    assert isinstance(course.id, type(None))  # ID not assigned yet
    assert inspect(course).attrs.keys() == {
        'id', 'code', 'name', 'credits', 'type', 'description',
        'prerequisites', 'required_by'
    }

def test_prerequisite_relationship():
    course = Course(code="CS102")
    prereq = Course(code="CS101")
    relation = Prerequisite(course=course, prereq=prereq)
    
    assert relation.course == course
    assert relation.prereq == prereq