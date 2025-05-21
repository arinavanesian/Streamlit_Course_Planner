from .database import SessionLocal
from .models import Course
from .repositories import CourseRepository

def init_courses():
    db = SessionLocal()
    repo = CourseRepository(db)


prereq_courses = [
    {
        "code": "CS111",
        "name": "Discrete Mathematics",
        "credits": 3,
        "type": "Prerequisite",
        "description": "Introduction to discrete mathematical structures"
    },
    {
        "code": "CS120",
        "name": "Intro to OOP",
        "credits": 3,
        "type": "Prerequisite",
        "description": "Introduction to object-oriented programming"
    },
    {
        "code": "CS121",
        "name": "Data Structures",
        "credits": 3,
        "type": "Prerequisite",
        "description": "Fundamental data structures and algorithms"
    },
    {
        "code": "CS130",
        "name": "Computer Organization",
        "credits": 3,
        "type": "Prerequisite",
        "description": "Computer architecture and organization"
    },
    {
        "code": "CS211",
        "name": "Algorithms",
        "credits": 3,
        "type": "Prerequisite", 
        "description": "Design and analysis of algorithms"
    },
    {
        "code": "IESM106",
        "name": "Probability and Statistics",
        "credits": 3,
        "type": "Prerequisite",
        "description": "Introduction to probability theory and statistics"
    }
]

core_courses = [
    {
        "code": "CS310",
        "name": "Theory of Computing",
        "credits": 3,
        "type": "Core",
        "description": "Formal languages, automata theory, computability"
    },
    {
        "code": "CS312",
        "name": "OOAD / Advanced OOP",
        "credits": 3,
        "type": "Core",
        "description": "Object-oriented analysis and design patterns"
    },
    {
        "code": "CS313",  # Changed duplicate CS312 to CS313
        "name": "Advanced Topics in Algorithms",
        "credits": 3,
        "type": "Core",
        "description": "Advanced algorithm design and analysis techniques"
    },
    {
        "code": "CS322",
        "name": "Software Engineering",
        "credits": 3,
        "type": "Core",
        "description": "Software development methodologies and best practices"
    },
    {
        "code": "CS326",
        "name": "Database Systems",
        "credits": 3,
        "type": "Core",
        "description": "Relational database design and implementation"
    },
    {
        "code": "CS340",
        "name": "Machine Learning",
        "credits": 3,
        "type": "Core",
        "description": "Fundamentals of machine learning algorithms"
    },
    {
        "code": "CS350",
        "name": "Software Project Management",
        "credits": 3,
        "type": "Core",
        "description": "Managing software projects and development teams"
    },
    {
        "code": "DS330",
        "name": "Deep Learning",
        "credits": 3,
        "type": "Core",
        "description": "Neural networks and deep learning architectures"
    },
    {
        "code": "CS395",
        "name": "Capstone Preparation",
        "credits": 1,  # Special 1-credit course
        "type": "Capstone",
        "description": "Preparation for capstone project (2nd year standing required)"
    },
    {
        "code": "CS396",
        "name": "Capstone Thesis",
        "credits": 3,
        "type": "Capstone",
        "description": "Final capstone project (or CS390 Capstone Practicum)"
    }
]
    # Insert prerequisite courses
    for course_data in prereq_courses:
        if not repo.get_by_code(course_data["code"]):
            repo.create(course_data)
            print(f"Added prerequisite course: {course_data['code']} - {course_data['name']}")
        else:
            print(f"Course {course_data['code']} already exists, skipping...")

    # Insert core courses
    for course_data in core_courses:
        if not repo.get_by_code(course_data["code"]):
            repo.create(course_data)
            print(f"Added course: {course_data['code']} - {course_data['name']}")
        else:
            print(f"Course {course_data['code']} already exists, skipping...")

    db.close()
    print("All courses have been inserted successfully!")

if __name__ == "__main__":
    init_courses()
