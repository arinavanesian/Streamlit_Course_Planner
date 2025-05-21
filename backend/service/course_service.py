from data.repositories import CourseRepository

class CourseService:
    def __init__(self, db):
        self.repo = CourseRepository(db)
    
    def list_courses(self):
        return self.repo.get_all()
    
    def get_course(self, code: str):
        return self.repo.get_by_code(code)