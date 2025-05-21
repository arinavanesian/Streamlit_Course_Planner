"""
API Layer Package
Exposes the FastAPI router for inclusion in the main app
"""
from .endpoints import router

__all__ = ["router"]
