from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.data.models import Course
from backend.data import get_db  
from backend.api import router
from backend.service.recommendation_service import RecommendationService

app = FastAPI()

app.include_router(router, prefix="/api/v1")


@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "Course Planner API"}


@app.get("/courses")
def list_courses(db: Session = Depends(get_db)):
    """List all courses"""
    return db.query(Course).all()


@app.get("/courses/{course_code}")
def get_course(course_code: str, db: Session = Depends(get_db)):
    """Get a specific course by code"""
    course = db.query(Course).filter(Course.code == course_code).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.post("/courses")
def create_course(
    code: str,
    name: str,
    credits: int,
    type: str,
    description: str = None,
    db: Session = Depends(get_db)
):
    """Create a new course"""
    existing = db.query(Course).filter(Course.code == code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Course code already exists")

    new_course = Course(
        code=code,
        name=name,
        credits=credits,
        type=type,
        description=description
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@app.post("/recommendations")
async def get_recommendations(student_info: dict, db: Session = Depends(get_db)):
    """
    Get course recommendations based on:
    - completed_courses: List[str]
    - interests: str
    - goals: str
    """
    try:
        recommendation_service = RecommendationService(db)
        recommendations, metadata = recommendation_service.generate_recommendation(student_info)
        return {"recommendations": recommendations, "metadata": metadata}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))