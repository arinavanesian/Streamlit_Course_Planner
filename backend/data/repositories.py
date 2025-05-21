from sqlalchemy.orm import Session
from .models import Course, Prerequisite

class CourseRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_code(self, code: str):
        return self.db.query(Course).filter(Course.code == code).first()

class PrerequisiteRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def add_prerequisite(self, course_code: str, prereq_code: str):
        course = self.db.query(Course).filter(Course.code == course_code).first()
        prereq = self.db.query(Course).filter(Course.code == prereq_code).first()
        
        if not course or not prereq:
            raise ValueError("Course or prerequisite not found")
            
        exists = self.db.query(Prerequisite).filter_by(
            course_id=course.id,
            prereq_id=prereq.id
        ).first()
        
        if exists:
            raise ValueError("Prerequisite relationship already exists")
            
        new_prereq = Prerequisite(course_id=course.id, prereq_id=prereq.id)
        self.db.add(new_prereq)
        return new_prereq
