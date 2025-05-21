"""
Service Layer Package
Exposes business logic services
"""
from .course_service import CourseService
from .recommendation_service import RecommendationService

__all__ = ["CourseService", "RecommendationService"]