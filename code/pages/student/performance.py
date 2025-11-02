# performance.py - Auto-extracted from app.py
import streamlit as st
import pandas as pd
import plotly.express as px


def display_student_performance():
    st.title("My Performance")
    
    # Course selector
    courses = ["All Courses", "Engineering 101", "Data Science Basics", "Physics Fundamentals"]
    selected_course = st.selectbox("Select Course", courses)
    
    # Time period selector
    time_periods = ["All Time", "This Semester", "Last 30 Days", "Last Week"]
    selected_period = st.selectbox("Time Period", time_periods)
    
    # Performance overview
    st.subheader("Performance Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Grade", "B+")
    with col2:
        st.metric("Average Score", "87%")
    with col3:
        st.metric("Submissions", "18/20")
    with col4:
        st.metric("Engagement", "Above Average", delta="15%")
    
    # Performance charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Grade Trend")
        # Mock grade data
        dates = pd.date_range(start='2025-01-01', periods=10, freq='W')
        grades = [85, 82, 88, 85, 90, 87, 91, 89, 92, 88]
        grade_data = pd.DataFrame({
            'Date': dates,
            'Grade': grades
        })
        st.line_chart(grade_data.set_index('Date'))
    
    with col2:
        st.subheader("Assessment Performance")
        # Mock assessment data
        assessment_types = ['Quiz', 'Homework', 'Project', 'Exam']
        scores = [92, 87, 78, 85]
        avg_scores = [85, 80, 82, 79]
        
        assessment_data = pd.DataFrame({
            'Type': assessment_types,
            'Your Score': scores,
            'Class Average': avg_scores
        })
        
        fig = px.bar(assessment_data, x='Type', y=['Your Score', 'Class Average'],
                    barmode='group', title='Your Performance vs. Class Average')
        st.plotly_chart(fig)
    
    # Detailed assessment history
    st.subheader("Assessment History")
    
    assessment_history = pd.DataFrame({
        'Date': ['Mar 15, 2025', 'Mar 1, 2025', 'Feb 15, 2025', 'Feb 1, 2025', 'Jan 15, 2025'],
        'Title': ['Midterm Exam', 'Project Phase 1', 'Quiz 3', 'Homework 2', 'Quiz 1'],
        'Type': ['Exam', 'Project', 'Quiz', 'Homework', 'Quiz'],
        'Score': ['88%', '92%', '85%', '90%', '82%'],
        'Feedback': ['Good work, improve on section 3', 'Excellent analysis', 'Review chapter 4', 'Well structured', 'Study definitions']
    })
    
    st.dataframe(assessment_history)
    
    # Strengths and improvement areas
    st.subheader("Strengths and Areas for Improvement")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Strengths")
        st.success("Problem-solving skills")
        st.success("Conceptual understanding")
        st.success("Project implementation")
    
    with col2:
        st.markdown("### Areas for Improvement")
        st.error("Time management")
        st.error("Theoretical foundation in Topic 4.2")
        st.error("Consistent practice")


