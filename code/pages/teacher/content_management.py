# content_management.py - Auto-extracted from app.py
import streamlit as st
import pandas as pd


def display_content_management():
    st.title("Content Management")
    
    # Class selector
    classes = ["Engineering 101", "Data Science Basics", "Advanced AI"]
    selected_class = st.selectbox("Select Class", classes, key="content_mgmt_class")

    # Content management tabs
    tab1, tab2, tab3 = st.tabs(["Course Structure", "Learning Materials", "Assessments"])

    with tab1:
        st.subheader("Course Structure")

        # Module list
        modules = pd.DataFrame({
            'Module': ['Module 1: Introduction', 'Module 2: Fundamentals', 'Module 3: Advanced Topics', 'Module 4: Applications', 'Module 5: Final Project'],
            'Topics': [3, 5, 4, 3, 1],
            'Status': ['Published', 'Published', 'Draft', 'Draft', 'Planned'],
            'Visibility': ['Visible', 'Visible', 'Hidden', 'Hidden', 'Hidden']
        })

        st.dataframe(modules)

        # Module editor
        st.subheader("Module Editor")
        selected_module = st.selectbox("Select Module", modules['Module'], key="module_editor_select")

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Module Title", value=selected_module, key="module_title")
            st.text_area("Description", value="This module covers the fundamental concepts...", key="module_desc")
            st.selectbox("Status", ["Draft", "Published", "Archived"], key="module_status")
            st.selectbox("Visibility", ["Hidden", "Visible"], key="module_visibility")
        
        with col2:
            st.markdown("### Module Settings")
            st.checkbox("Require Sequential Progression", value=True, key="module_req_seq")
            st.checkbox("Enable AI Recommendations", value=True, key="module_ai_rec")
            st.number_input("Estimated Completion Time (hours)", value=10, key="module_est_time")
            st.date_input("Release Date", key="module_release_date")

        st.button("Save Module", key="save_module_btn")

    with tab2:
        st.subheader("Learning Materials")

        # Material types
        material_type = st.selectbox("Material Type", ["All", "Video", "Document", "Interactive", "Assessment"], key="material_type_filter")

        # Material list
        materials = pd.DataFrame({
            'Title': ['Introduction to Course', 'Fundamental Concepts', 'Interactive Simulation', 'Practice Problems', 'Case Study'],
            'Type': ['Video', 'Document', 'Interactive', 'Assessment', 'Document'],
            'Module': ['Module 1', 'Module 1', 'Module 2', 'Module 2', 'Module 3'],
            'Status': ['Published', 'Published', 'Draft', 'Published', 'Draft']
        })

        if material_type != "All":
            materials = materials[materials['Type'] == material_type]

        st.dataframe(materials)

        # Material uploader
        st.subheader("Add New Material")

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Title", key="material_title")
            st.selectbox("Material Type", ["Video", "Document", "Interactive", "Assessment"], key="material_type_new")
            st.selectbox("Associated Module", modules['Module'], key="material_module")
            st.text_area("Description", key="material_desc")

        with col2:
            st.file_uploader("Upload File", type=["pdf", "docx", "mp4", "ppt", "html"], key="material_file")
            st.text_input("External URL (if applicable)", key="material_url")
            st.number_input("Estimated Completion Time (minutes)", key="material_time")
            st.selectbox("Initial Status", ["Draft", "Published"], key="material_status")
        
        st.button("Add Material", key="add_material_btn")

    with tab3:
        st.subheader("Assessments")

        # Assessment types
        assessment_type = st.selectbox("Assessment Type", ["All", "Quiz", "Homework", "Exam", "Project"], key="assessment_type_filter")

        # Assessment list
        assessments = pd.DataFrame({
            'Title': ['Quiz 1: Fundamentals', 'Homework 1', 'Midterm Exam', 'Project Proposal', 'Final Exam'],
            'Type': ['Quiz', 'Homework', 'Exam', 'Project', 'Exam'],
            'Due Date': ['Jan 30, 2025', 'Feb 15, 2025', 'Mar 1, 2025', 'Apr 10, 2025', 'May 5, 2025'],
            'Status': ['Published', 'Published', 'Draft', 'Draft', 'Planned']
        })

        if assessment_type != "All":
            assessments = assessments[assessments['Type'] == assessment_type]

        st.dataframe(assessments)

        # Assessment creator
        st.subheader("Create Assessment")

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Assessment Title", key="assessment_title")
            st.selectbox("Assessment Type", ["Quiz", "Homework", "Exam", "Project"], key="assessment_type_new")
            st.selectbox("Associated Module", modules['Module'], key="assessment_module")
            st.date_input("Due Date", key="assessment_due_date")

        with col2:
            st.number_input("Points", value=100, key="assessment_points")
            st.number_input("Time Limit (minutes)", value=60, key="assessment_time_limit")
            st.checkbox("Allow Multiple Attempts", key="assessment_multiple_attempts")
            st.selectbox("Initial Status", ["Draft", "Published"], key="assessment_status")

        st.button("Create Assessment", key="create_assessment_btn")
        st.button("Question Bank", key="question_bank_btn")


