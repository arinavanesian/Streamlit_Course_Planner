from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    credits = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)
    description = Column(Text)
    
    prerequisites = relationship(
        "Prerequisite",
        foreign_keys="[Prerequisite.course_id]",
        back_populates="course"
    )
    
    required_by = relationship(
        "Prerequisite",
        foreign_keys="[Prerequisite.prereq_id]",
        back_populates="prereq"
    )

class Prerequisite(Base):
    __tablename__ = "prerequisites"
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    prereq_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
        course = relationship("Course", foreign_keys=[course_id], back_populates="prerequisites")
    prereq = relationship("Course", foreign_keys=[prereq_id], back_populates="required_by")