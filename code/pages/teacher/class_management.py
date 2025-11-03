# class_management.py - Auto-extracted from app.py
import streamlit as st
import pandas as pd
import numpy as np


def display_class_management():
    st.title("Class Management")
    
    # Mock class data
    classes = pd.DataFrame({
        'Class ID': [101, 102, 103],
        'Class Name': ['Engineering 101', 'Data Science Basics', 'Advanced AI'],
        'Students': [25, 18, 12],
        'Start Date': ['Jan 15, 2025', 'Feb 1, 2025', 'Mar 10, 2025'],
        'End Date': ['May 15, 2025', 'Jun 1, 2025', 'Jul 10, 2025'],
        'Status': ['Active', 'Active', 'Upcoming']
    })
    
    # Class selector
    selected_class = st.selectbox("Select Class", classes['Class Name'])
    selected_class_data = classes[classes['Class Name'] == selected_class].iloc[0]
    
    # Class details
    st.header(f"{selected_class} Details")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Students Enrolled", selected_class_data['Students'])
    with col2:
        st.metric("Start Date", selected_class_data['Start Date'])
    with col3:
        st.metric("End Date", selected_class_data['End Date'])
    
    # Class management tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Students", "Content", "Assessments", "Settings"])
    
    with tab1:
        st.subheader("Enrolled Students")
        # Mock student data
        students = pd.DataFrame({
            'Student ID': range(1001, 1001 + selected_class_data['Students']),
            'Name': [f"Student {i}" for i in range(1, selected_class_data['Students'] + 1)],
            'Progress': np.random.uniform(30, 95, selected_class_data['Students']),
            'Last Active': [f"{i} days ago" for i in np.random.randint(1, 10, selected_class_data['Students'])],
            'Risk Level': np.random.choice(['Low', 'Medium', 'High'], selected_class_data['Students'], p=[0.7, 0.2, 0.1])
        })
        
        # Filter options
        risk_filter = st.multiselect("Filter by Risk Level", ['Low', 'Medium', 'High'], default=[])
        if risk_filter:
            students = students[students['Risk Level'].isin(risk_filter)]
        
        st.dataframe(students)
        
        # Bulk actions
        col1, col2 = st.columns(2)
        with col1:
            st.button("Send Message to Selected")
        with col2:
            st.button("Export Student List")
    
    with tab2:
        st.subheader("Course Content")
        
        # Mock modules
        modules = pd.DataFrame({
            'Module': ['Introduction', 'Fundamentals', 'Advanced Concepts', 'Practical Applications', 'Final Project'],
            'Topics': [3, 5, 4, 6, 2],
            'Status': ['Published', 'Published', 'Draft', 'Draft', 'Planned'],
            'Avg. Completion': ['95%', '78%', '42%', '15%', '0%']
        })
        
        st.dataframe(modules)
        
        st.button("Add New Module")
        st.button("Edit Selected Module")
    
    with tab3:
        st.subheader("Assessments")
        
        # Mock assessments
        assessments = pd.DataFrame({
            'Title': ['Quiz 1', 'Homework 1', 'Midterm Exam', 'Project Proposal', 'Final Exam'],
            'Type': ['Quiz', 'Assignment', 'Exam', 'Project', 'Exam'],
            'Due Date': ['Jan 30, 2025', 'Feb 15, 2025', 'Mar 1, 2025', 'Apr 10, 2025', 'May 5, 2025'],
            'Status': ['Completed', 'Completed', 'Open', 'Upcoming', 'Planned'],
            'Avg. Score': ['82%', '76%', '-', '-', '-']
        })
        
        st.dataframe(assessments)
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Create New Assessment")
        with col2:
            st.button("Grade Submissions")
    
    with tab4:
        st.subheader("Class Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Class Name", value=selected_class)
            st.date_input("Start Date")
            st.date_input("End Date")
        
        with col2:
            st.selectbox("Enrollment Type", ["Open", "Invitation Only", "Approval Required"])
            st.number_input("Maximum Students", value=30)
            st.checkbox("Enable AI Recommendations", value=True)
        
        st.text_area("Class Description", "A comprehensive introduction to engineering principles...")
        st.button("Save Settings")


