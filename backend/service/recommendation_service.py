import google.generativeai as genai
from typing import List, Dict, Optional, Tuple
from data.repositories import CourseRepository
from data.models import Course
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self, db_session):
        """
        Initialize recommendation service with DB session and AI configuration
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.course_repo = CourseRepository(db_session)
        self._configure_gemini()
        self.system_prompt = self._load_system_prompt()

    def _configure_gemini(self):
        """Configure Gemini API with safety settings"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        
        # Configure safety settings
        safety_settings = {
            'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
            'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
            'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
            'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE'
        }
        
        self.model = genai.GenerativeModel(
            'gemini-pro',
            safety_settings=safety_settings
        )

    def _load_system_prompt(self) -> str:
        """Load the base system prompt"""
        return """
        You are an academic advisor for the American University of Armenia (AUA) Computer Science program.
        Your task is to recommend courses based on:
        - Completed prerequisites
        - Student interests
        - Academic goals
        - Current progress
        
        Always consider:
        1. Prerequisite satisfaction
        2. Course difficulty progression
        3. Relevance to stated interests
        4. Alignment with career/academic goals
        
        Provide recommendations in this format:
        ### [Course Code]: [Course Name]
        - **Why Recommended**: [2-3 sentence justification]
        - **Prerequisites Met**: [List]
        - **Potential Challenges**: [If any]
        """

    def generate_recommendation(self, student_info: Dict) -> Tuple[str, Dict]:
        """
        Generate and validate course recommendations
        
        Args:
            student_info: {
                "completed_courses": List[str],
                "interests": str,
                "goals": str,
                "current_semester": Optional[int],
                "max_courses": Optional[int] (default:4)
            }
            
        Returns:
            tuple: (markdown_response, metadata)
        """
        try:
            # Validate input
            if not student_info.get('completed_courses'):
                raise ValueError("At least one completed course is required")
            
            # Get course data
            courses = self.course_repo.get_all()
            available_courses = self._format_course_list(courses)
            
            # Generate prompt
            prompt = self._build_prompt(student_info, available_courses)
            logger.info(f"Generated prompt: {prompt[:200]}...")
            
            # Get AI response
            start_time = datetime.now()
            response = self._get_gemini_response(prompt)
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Validate and format
            formatted = self._format_response(response)
            
            # Generate metadata
            metadata = {
                "generated_at": datetime.now().isoformat(),
                "processing_seconds": processing_time,
                "courses_considered": len(courses),
                "student_profile": {
                    k: v for k, v in student_info.items() 
                    if k != 'completed_courses'
                }
            }
            
            return formatted, metadata
            
        except Exception as e:
            logger.error(f"Recommendation failed: {str(e)}")
            return self._error_response(str(e)), {"error": True}

    def _format_course_list(self, courses: List[Course]) -> str:
        """Format courses with prerequisites and descriptions"""
        return "\n\n".join(
            f"""**{course.code}**: {course.name}
- Credits: {course.credits}
- Type: {course.type}
- Prerequisites: {self._get_prereqs(course)}
- Description: {course.description or 'Not available'}"""
            for course in sorted(courses, key=lambda x: x.code)
        )

    def _get_prereqs(self, course: Course) -> str:
        """Format prerequisites with completion check"""
        if not course.prerequisites:
            return "None"
        return ", ".join(
            f"{p.prereq.code} ({'✓' if p.prereq.code in self._completed_courses else '✗'})"
            for p in course.prerequisites
        )

    def _build_prompt(self, student_info: Dict, available_courses: str) -> str:
        """Construct the complete prompt"""
        self._completed_courses = student_info.get('completed_courses', [])
        
        return f"""
        {self.system_prompt}
        
        **Student Profile**:
        - Completed Courses: {', '.join(self._completed_courses)}
        - Interests: {student_info.get('interests', 'Not specified')}
        - Goals: {student_info.get('goals', 'Not specified')}
        - Current Semester: {student_info.get('current_semester', 'Not specified')}
        
        **Available Courses**:
        {available_courses}
        
        Please recommend {student_info.get('max_courses', 4)} courses.
        Prioritize courses where all prerequisites are met (marked with ✓).
        """

    def _get_gemini_response(self, prompt: str) -> str:
        """Get response with enhanced error handling"""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": 2000,
                    "temperature": 0.7
                }
            )
            if not response.text:
                raise ValueError("Empty response from Gemini API")
            return response.text
        except Exception as e:
            logger.exception("Gemini API call failed")
            raise RuntimeError(f"AI service unavailable: {str(e)}")

    def _format_response(self, raw_response: str) -> str:
        """Format and sanitize the response"""
        # Remove any potentially harmful HTML/JS
        sanitized = raw_response.replace("<", "&lt;").replace(">", "&gt;")
        
        return f"""
# AUA Course Recommendations  
*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*  

{sanitized}

---
*This is an AI-generated recommendation. Please verify with your academic advisor.*
        """

    def _error_response(self, error_msg: str) -> str:
        """Generate user-friendly error message"""
        return f"""
# Recommendation Error

We couldn't generate recommendations at this time.  

**Reason**: {error_msg}  

Please try again later or contact support.
        """
