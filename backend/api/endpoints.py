from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.data.database import get_db
from backend.service.course_service import CourseService
router = APIRouter()

@router.get("/courses")
def list_courses(db: Session = Depends(get_db)):
    return CourseService(db).list_courses()