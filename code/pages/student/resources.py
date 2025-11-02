# resources.py - Auto-extracted from app.py
import streamlit as st
import pandas as pd


def display_resources():
    st.title("Learning Resources")
    
    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("Search Resources")
    with col2:
        resource_type = st.selectbox("Type", ["All", "Video", "Article", "Practice", "Document"])
    
    # Resource tabs
    tab1, tab2, tab3 = st.tabs(["Recommended", "Course Materials", "Additional Resources"])
    
    with tab1:
        st.subheader("Recommended for You")
        
        # Mock recommendations
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Matrix Operations")
            st.image("https://via.placeholder.com/150", width=150)
            st.markdown("**Type:** Video Tutorial")
            st.markdown("**Duration:** 15 minutes")
            st.markdown("**Relevance:** High - Based on your current learning path")
            st.button("Watch Now", key="watch1")
        
        with col2:
            st.markdown("### Problem-Solving Techniques")
            st.image("https://via.placeholder.com/150", width=150)
            st.markdown("**Type:** Interactive Tutorial")
            st.markdown("**Duration:** 25 minutes")
            st.markdown("**Relevance:** Medium - Helps with your upcoming assignment")
            st.button("Start Tutorial", key="tutorial1")
        
        with col3:
            st.markdown("### Real-World Applications")
            st.image("https://via.placeholder.com/150", width=150)
            st.markdown("**Type:** Case Study")
            st.markdown("**Duration:** 20 minutes")
            st.markdown("**Relevance:** Medium - Supplements your current topic")
            st.button("Read Case Study", key="case1")
    
    with tab2:
        st.subheader("Course Materials")
        
        # Mock course materials
        materials = pd.DataFrame({
            'Title': ['Lecture 1: Introduction', 'Lecture 2: Fundamentals', 'Lab Manual', 'Homework Guidelines', 'Textbook Chapter 3'],
            'Type': ['Video', 'Video', 'Document', 'Document', 'Reading'],
            'Date Added': ['Jan 15, 2025', 'Jan 22, 2025', 'Jan 10, 2025', 'Jan 5, 2025', 'Jan 22, 2025'],
            'Duration/Length': ['45 min', '50 min', '12 pages', '3 pages', '28 pages']
        })
        
        st.dataframe(materials)
    
    with tab3:
        st.subheader("Additional Resources")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Online References")
            references = [
                "Engineering Fundamentals Database",
                "Khan Academy: Linear Algebra",
                "MIT OpenCourseWare",
                "Interactive Math Tutorials",
                "Scientific Paper Repository"
            ]
            
            for ref in references:
                st.markdown(f"- {ref}")
        
        with col2:
            st.markdown("### Community Resources")
            st.markdown("- Student Discussion Forum")
            st.markdown("- Study Group Directory")
            st.markdown("- Peer Tutoring Services")
            st.markdown("- Alumni Mentorship Program")


