from .database import SessionLocal
from .repositories import CourseRepository, PrerequisiteRepository

def add_prerequisite(repo: PrerequisiteRepository, course_code: str, prereq_code: str):
    try:
        repo.add_prerequisite(course_code, prereq_code)
        print(f"Added prerequisite: {prereq_code} -> {course_code}")
    except ValueError as e:
        print(f"Error: {str(e)} ({prereq_code} -> {course_code})")

def init_prerequisites():
    db = SessionLocal()
    course_repo = CourseRepository(db)
    prereq_repo = PrerequisiteRepository(db)
    
    # Format: (course code, prerequisite course code)
    prerequisites = [
        ("CS340", "IESM106"),  # Machine Learning requires Probability
        ("CS310", "CS111"),    # Theory of Computing requires Discrete Math
        ("CS312", "CS120"),    # OOAD requires Intro OOP
        ("CS313", "CS121"),    # Advanced Algorithms requires Data Structures
        ("CS326", "CS121"),    # Database Systems requires Data Structures
        ("CS322", "CS130"),    # Software Engineering requires Computer Org
        ("CS313", "CS211"),    # Advanced Algorithms requires Algorithms
        ("CS340", "CS211"),    # Machine Learning requires Algorithms
        ("DS330", "CS340")     # Deep Learning requires Machine Learning
    ]
    
    for course_code, prereq_code in prerequisites:
        add_prerequisite(prereq_repo, course_code, prereq_code)
    
    db.commit()
    db.close()
    print("All prerequisites added successfully!")

if __name__ == "__main__":
    init_prerequisites()
