"""
Data Layer Package
Exposes database components and repositories
"""
from .database import Base, SessionLocal, get_db, engine
from .models import Course, Prerequisite
from .repositories import CourseRepository, PrerequisiteRepository

# Optional: Auto-initialize tables on import (remove if using migrations)
Base.metadata.create_all(bind=engine)

__all__ = [
    "Base",
    "SessionLocal",
    "get_db",
    "engine",
    "Course",
    "Prerequisite",
    "CourseRepository", 
    "PrerequisiteRepository"
]