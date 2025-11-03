# dashboard.py - Dashboard page for all user roles
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from modules.auth import load_users


def display_dashboard():
    """Display dashboard based on user role"""
    st.title("Dashboard")

    # Different dashboard content based on role
    if st.session_state.role == "admin":
        display_admin_dashboard()
    elif st.session_state.role == "teacher":
        display_teacher_dashboard()
    else:  # student
        display_student_dashboard()


def display_admin_dashboard():
    """Admin dashboard with system overview"""
    st.header("System Overview")

    # Mock data for demonstration
    users = load_users()
    student_count = len(users[users['role'] == 'student'])
    teacher_count = len(users[users['role'] == 'teacher'])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Students", student_count)
    with col2:
        st.metric("Total Teachers", teacher_count)
    with col3:
        st.metric("Active Courses", 10)  # Mock data

    # System health
    st.subheader("System Health")
    health_data = {
        'Component': ['Database', 'API Server', 'ML Models', 'Storage'],
        'Status': ['Healthy', 'Healthy', 'Healthy', 'Healthy'],
        'Load': [25, 40, 35, 15]
    }
    health_df = pd.DataFrame(health_data)
    st.dataframe(health_df)

    # Recent activity
    st.subheader("Recent Activity")
    activity_data = {
        'Time': ['10:45 AM', '09:30 AM', '09:15 AM', '08:00 AM', 'Yesterday'],
        'User': ['teacher1', 'student5', 'admin', 'student12', 'teacher3'],
        'Activity': [
            'Created new course',
            'Completed assessment',
            'System backup',
            'Missed deadline',
            'Updated course content'
        ]
    }
    st.dataframe(pd.DataFrame(activity_data))


def display_teacher_dashboard():
    """Teacher dashboard with class overview"""
    st.header("Teacher Dashboard")

    st.subheader("Your Classes")
    # Display mock class list
    classes = pd.DataFrame({
        'Class Name': ['Engineering 101', 'Data Science Basics', 'Advanced AI'],
        'Students': [25, 18, 12],
        'Average Progress': ['65%', '72%', '45%'],
        'At-Risk Students': [3, 1, 4]
    })
    st.dataframe(classes)

    # Class engagement
    st.subheader("Class Engagement")
    engagement_data = pd.DataFrame({
        'Week': list(range(1, 11)),
        'Engineering 101': np.random.uniform(60, 90, 10),
        'Data Science Basics': np.random.uniform(65, 95, 10),
        'Advanced AI': np.random.uniform(50, 85, 10)
    })
    st.line_chart(engagement_data.set_index('Week'))

    # Recent submissions
    st.subheader("Recent Submissions")
    submissions = pd.DataFrame({
        'Student': ['John D.', 'Maria S.', 'Alex T.', 'Laura H.', 'Kevin P.'],
        'Assignment': ['Homework 3', 'Project Proposal', 'Quiz 2', 'Final Project', 'Homework 4'],
        'Submitted': ['2 hours ago', '1 day ago', '2 days ago', '2 days ago', '3 days ago'],
        'Status': ['Pending', 'Graded', 'Graded', 'Pending', 'Graded'],
        'Score': [None, '92%', '78%', None, '88%']
    })
    st.dataframe(submissions)


def display_student_dashboard():
    """Student dashboard with progress overview"""
    st.header("Student Dashboard")

    # Get student-specific data
    from modules.student_data import get_student_profile
    username = st.session_state.get('username', 'student1')
    student_profile = get_student_profile(username)

    # Use default data if no profile found
    if not student_profile:
        student_profile = {
            'overall_progress': 68,
            'assignments_completed': 12,
            'assignments_total': 20,
            'course_progress': [
                {'name': 'Engineering 101', 'progress': 68},
                {'name': 'Data Science Basics', 'progress': 62},
                {'name': 'Physics Fundamentals', 'progress': 75},
            ],
            'next_deadlines': [
                {'title': 'Assignment 3', 'due': 'in 2 days'},
                {'title': 'Quiz 5', 'due': 'in 5 days'},
                {'title': 'Project Milestone', 'due': 'in 1 week'},
            ],
            'weekly_study_hours': [2.5, 1.5, 3.0, 2.0, 1.0, 4.0, 2.5],
            'recommendations': []
        }

    # Progress overview
    st.subheader("Your Progress")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Overall Progress", f"{student_profile['overall_progress']}%")
        st.metric("Assignments Completed",
                  f"{student_profile['assignments_completed']}/{student_profile['assignments_total']}")

        # Progress by course
        st.subheader("Progress by Course")
        course_progress = pd.DataFrame(student_profile['course_progress'])
        course_progress.rename(columns={'name': 'Course', 'progress': 'Progress'}, inplace=True)

        fig = px.bar(course_progress, x='Course', y='Progress', text='Progress',
                     color='Progress', color_continuous_scale='blues')
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Next Deadlines")
        for deadline in student_profile['next_deadlines']:
            # Check if overdue
            if 'OVERDUE' in deadline['title']:
                st.error(f"{deadline['title']}: {deadline['due']}")
            elif 'tomorrow' in deadline['due'] or 'day ago' in deadline['due']:
                st.warning(f"{deadline['title']}: {deadline['due']}")
            else:
                st.info(f"{deadline['title']}: {deadline['due']}")

        # Study time
        st.subheader("Weekly Study Time")
        study_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Hours': student_profile['weekly_study_hours']
        })
        st.bar_chart(study_data.set_index('Day'))

    # Recommendations
    st.subheader("Personalized Recommendations")

    if student_profile.get('recommendations'):
        cols = st.columns(3)
        for idx, rec in enumerate(student_profile['recommendations']):
            with cols[idx]:
                st.markdown(f"{rec['icon']} **{rec['title']}**")
                st.markdown(rec['content'])
                st.markdown(f"_{rec['reason']}_")
    else:
        # Fallback recommendations
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("📘 **Review Material**")
            st.markdown("Data Structures: Linked Lists")
            st.markdown("_Recommended based on recent quiz performance_")
        with col2:
            st.markdown("📝 **Practice Exercise**")
            st.markdown("Algorithm Efficiency Analysis")
            st.markdown("_Helps prepare for your upcoming assignment_")
        with col3:
            st.markdown("🎬 **Supplementary Resource**")
            st.markdown("Video: Understanding Big O Notation")
            st.markdown("_Aligns with your current learning path_")
