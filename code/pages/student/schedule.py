# schedule.py - Auto-extracted from app.py
import streamlit as st
import datetime
import pandas as pd


def display_schedule():
    st.title("Schedule Manager")
    
    # Role-specific content
    if st.session_state.role == "student":
        st.subheader("My Schedule")
        
        # Calendar view
        st.markdown("### Calendar View")
        current_month = datetime.datetime.now().strftime("%B %Y")
        st.markdown(f"**{current_month}**")
        
        # Simple calendar representation (would be replaced with a proper calendar widget in production)
        calendar_data = [
            ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            ["1", "2", "3", "4", "5", "6", "7"],
            ["8", "9", "10", "11", "12", "13", "14"],
            ["15", "16", "17", "18", "19", "20", "21"],
            ["22", "23", "24", "25", "26", "27", "28"],
            ["29", "30", "31", "", "", "", ""]
        ]
        
        # Add some event indicators
        calendar_data[1][2] = "3 📝"  # Assignment due
        calendar_data[2][4] = "12 📚"  # Quiz
        calendar_data[3][1] = "16 📊"  # Project deadline
        
        calendar_df = pd.DataFrame(calendar_data[1:], columns=calendar_data[0])
        st.table(calendar_df)
        
        # Upcoming deadlines
        st.subheader("Upcoming Deadlines")
        deadlines = pd.DataFrame({
            'Course': ['Engineering 101', 'Data Science', 'Engineering 101', 'Physics'],
            'Assignment': ['Homework 3', 'Project Proposal', 'Midterm Exam', 'Lab Report'],
            'Due Date': ['Apr 3, 2025', 'Apr 12, 2025', 'Apr 16, 2025', 'Apr 20, 2025'],
            'Status': ['Pending', 'Not Started', 'Not Started', 'Not Started'],
            'Priority': ['High', 'Medium', 'High', 'Medium']
        })
        
        st.dataframe(deadlines)
        
        # Schedule adjustment
        st.subheader("Schedule Adjustment")
        
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Assignment", deadlines['Assignment'])
            st.date_input("Request New Due Date")
            st.selectbox("Reason", ["Illness", "Family Emergency", "Technical Issues", "Workload Conflict", "Other"])
            st.text_area("Additional Details")
            st.button("Submit Extension Request")
        
        with col2:
            st.markdown("### Extension Policy")
            st.info("""
            - Requests must be submitted at least 48 hours before the deadline
            - Supporting documentation may be required
            - Maximum extension is typically 7 days
            - Each student has 3 extension tokens per semester
            """)
            st.markdown("**Your remaining tokens:** 2")
    
    elif st.session_state.role == "teacher":
        st.subheader("Class Schedule Management")
        
        # Class selector
        classes = ["Engineering 101", "Data Science Basics", "Advanced AI"]
        selected_class = st.selectbox("Select Class", classes)
        
        # Assessment schedule
        st.markdown("### Assessment Schedule")
        
        assessments = pd.DataFrame({
            'Assessment': ['Quiz 1', 'Homework 1', 'Midterm', 'Project Proposal', 'Final Exam'],
            'Type': ['Quiz', 'Assignment', 'Exam', 'Project', 'Exam'],
            'Due Date': ['Jan 30, 2025', 'Feb 15, 2025', 'Mar 1, 2025', 'Apr 10, 2025', 'May 5, 2025'],
            'Status': ['Completed', 'Completed', 'Open', 'Scheduled', 'Scheduled']
        })
        
        st.dataframe(assessments)
        
        # Schedule management
        st.markdown("### Modify Schedule")
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Assessment", assessments['Assessment'])
            st.date_input("Current Due Date", value=datetime.datetime(2025, 3, 1))
            st.date_input("New Due Date")
            st.checkbox("Notify Students")
            st.text_area("Notification Message")
            st.button("Update Schedule")
        
        with col2:
            st.markdown("### Workload Analysis")
            st.info("Current schedule shows potential workload peak in week of March 1. Consider redistributing assessments.")
            
            # Simple workload visualization
            weeks = [f"Week {i}" for i in range(1, 11)]
            workload = [1, 2, 1, 0, 3, 1, 1, 2, 0, 2]
            
            workload_data = pd.DataFrame({
                'Week': weeks,
                'Assessments': workload
            })
            
            st.bar_chart(workload_data.set_index('Week'))
        
        # Extension requests
        st.markdown("### Extension Requests")
        
        extension_requests = pd.DataFrame({
            'Student': ['John D.', 'Maria S.', 'Alex T.'],
            'Assignment': ['Homework 3', 'Midterm', 'Project Proposal'],
            'Current Due': ['Apr 3, 2025', 'Mar 1, 2025', 'Apr 10, 2025'],
            'Requested Due': ['Apr 7, 2025', 'Mar 5, 2025', 'Apr 17, 2025'],
            'Reason': ['Illness', 'Family Emergency', 'Technical Issues'],
            'Status': ['Pending', 'Pending', 'Pending']
        })
        
        st.dataframe(extension_requests)
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Approve Selected")
        with col2:
            st.button("Deny Selected")


