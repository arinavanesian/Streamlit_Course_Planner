import streamlit as st
import requests
from datetime import datetime
import os

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://backend:8000/api/v1")
COMPLETED_COURSES_OPTIONS = [
    "CS111", "CS120", "CS121", "CS130", "CS211", "IESM106"
]

# Page Configuration
st.set_page_config(
    page_title="AUA Course Planner",
    page_icon="📚",
    layout="wide"
)

def initialize_session_state():
    """Initialize session state variables"""
    if "recommendation" not in st.session_state:
        st.session_state.recommendation = None
    if "metadata" not in st.session_state:
        st.session_state.metadata = None
    if "last_submit" not in st.session_state:
        st.session_state.last_submit = None

def get_recommendation(student_info):
    """Call recommendation API endpoint"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/recommendations",
            json=student_info,
            timeout=10  # 10 seconds timeout
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {str(e)}")
        return None

def display_recommendation():
    """Display recommendation with metadata"""
    if st.session_state.recommendation:
        st.markdown(st.session_state.recommendation)
        
        with st.expander("Recommendation Details"):
            st.write(f"**Generated at**: {st.session_state.metadata.get('generated_at')}")
            st.write(f"**Processing time**: {st.session_state.metadata.get('processing_seconds', 0):.2f} seconds")
            st.write(f"**Courses considered**: {st.session_state.metadata.get('courses_considered', 0)}")
            
            st.json(st.session_state.metadata)

def main():
    initialize_session_state()
    
    # Header
    st.title("📚 AUA Computer Science Course Planner")
    st.markdown("Get personalized course recommendations based on your academic progress and goals")
    
    # Recommendation Form
    with st.form("recommendation_form"):
        cols = st.columns(2)
        
        with cols[0]:
            completed_courses = st.multiselect(
                "Completed Courses",
                COMPLETED_COURSES_OPTIONS,
                help="Select all courses you've successfully completed"
            )
            
            interests = st.selectbox(
                "Primary Interest Area",
                ["AI/Machine Learning", "Software Engineering", "Systems", "Data Science", "Other"],
                index=0
            )
            
        with cols[1]:
            current_semester = st.number_input(
                "Current Semester",
                min_value=1,
                max_value=8,
                value=3,
                help="Your current semester of study"
            )
            
            goals = st.selectbox(
                "Primary Goal",
                ["Industry Career", "Research", "Graduate School", "Entrepreneurship"],
                index=0
            )
        
        # Additional options
        with st.expander("Advanced Options"):
            max_courses = st.slider(
                "Maximum Recommendations",
                min_value=1,
                max_value=6,
                value=4
            )
        
        submitted = st.form_submit_button("Get Recommendations")
        
        if submitted:
            with st.spinner("Generating recommendations..."):
                student_info = {
                    "completed_courses": completed_courses,
                    "interests": interests,
                    "goals": goals,
                    "current_semester": current_semester,
                    "max_courses": max_courses
                }
                
                result = get_recommendation(student_info)
                
                if result:
                    st.session_state.recommendation = result.get("recommendation")
                    st.session_state.metadata = result.get("metadata")
                    st.session_state.last_submit = datetime.now()
                    st.success("Recommendations generated successfully!")
                else:
                    st.error("Failed to generate recommendations. Please try again.")

    # Display results
    if st.session_state.recommendation:
        st.divider()
        st.subheader("Your Recommended Courses")
        display_recommendation()
        
        # Download button
        timestamp = st.session_state.last_submit.strftime("%Y%m%d_%H%M")
        st.download_button(
            label="Download Recommendations",
            data=st.session_state.recommendation,
            file_name=f"aua_course_recommendations_{timestamp}.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    main()