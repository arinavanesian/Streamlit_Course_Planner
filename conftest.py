import pytest
from backend.data.database import Base, engine, SessionLocal
from backend.data.models import Course, Prerequisite

@pytest.fixture
def db_session():
    Base.metadata.create_all(engine)
    session = SessionLocal()
    yield session
    session.rollback()
    Base.metadata.drop_all(engine)
    session.close()