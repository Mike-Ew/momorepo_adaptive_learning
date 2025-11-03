# schedule.py - Schedule management with interactive calendar
import streamlit as st
import datetime
import pandas as pd
from streamlit_calendar import calendar as st_calendar


def display_schedule():
    """Display schedule with interactive calendar for students and teachers"""
    st.title("Schedule Manager")

    # Role-specific content
    if st.session_state.role == "student":
        display_student_schedule()
    elif st.session_state.role == "teacher":
        display_teacher_schedule()


def display_student_schedule():
    """Student schedule view with interactive calendar"""
    st.subheader("My Schedule")

    # Calendar view with streamlit-calendar
    st.markdown("### Calendar View")

    # Prepare events for the calendar
    events = [
        {
            "title": "📝 Homework 3 Due",
            "start": "2025-11-05",
            "end": "2025-11-05",
            "backgroundColor": "#FF6B6B",
            "borderColor": "#FF6B6B",
        },
        {
            "title": "📚 Quiz 5",
            "start": "2025-11-08T14:00:00",
            "end": "2025-11-08T15:00:00",
            "backgroundColor": "#4ECDC4",
            "borderColor": "#4ECDC4",
        },
        {
            "title": "📊 Project Milestone",
            "start": "2025-11-12",
            "end": "2025-11-12",
            "backgroundColor": "#95E1D3",
            "borderColor": "#95E1D3",
        },
        {
            "title": "🎓 Midterm Exam",
            "start": "2025-11-16T10:00:00",
            "end": "2025-11-16T12:00:00",
            "backgroundColor": "#F38181",
            "borderColor": "#F38181",
        },
        {
            "title": "📖 Lab Report Due",
            "start": "2025-11-20",
            "end": "2025-11-20",
            "backgroundColor": "#FECA57",
            "borderColor": "#FECA57",
        },
        {
            "title": "💻 Coding Assignment",
            "start": "2025-11-25",
            "end": "2025-11-25",
            "backgroundColor": "#48DBFB",
            "borderColor": "#48DBFB",
        },
        {
            "title": "📝 Final Project Proposal",
            "start": "2025-11-28",
            "end": "2025-11-28",
            "backgroundColor": "#FF9FF3",
            "borderColor": "#FF9FF3",
        },
    ]

    # Calendar configuration
    calendar_options = {
        "editable": False,
        "selectable": True,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay,listWeek",
        },
        "initialView": "dayGridMonth",
        "slotMinTime": "08:00:00",
        "slotMaxTime": "20:00:00",
        "height": 650,
    }

    # Display calendar
    calendar_result = st_calendar(
        events=events,
        options=calendar_options,
        key="student_calendar"
    )

    # Show event details if clicked
    if calendar_result.get("eventClick"):
        st.info(f"📅 Selected: {calendar_result['eventClick']['event']['title']}")

    # Upcoming deadlines
    st.markdown("---")
    st.subheader("📋 Upcoming Deadlines")

    deadlines = pd.DataFrame({
        'Course': ['Engineering 101', 'Data Science', 'Engineering 101', 'Physics', 'Engineering 101', 'Data Science', 'Physics'],
        'Assignment': ['Homework 3', 'Quiz 5', 'Project Milestone', 'Midterm Exam', 'Lab Report', 'Coding Assignment', 'Final Project Proposal'],
        'Due Date': ['Nov 5, 2025', 'Nov 8, 2025', 'Nov 12, 2025', 'Nov 16, 2025', 'Nov 20, 2025', 'Nov 25, 2025', 'Nov 28, 2025'],
        'Status': ['In Progress', 'Not Started', 'Not Started', 'Not Started', 'Not Started', 'Not Started', 'Not Started'],
        'Priority': ['🔴 High', '🟡 Medium', '🟢 Low', '🔴 High', '🟡 Medium', '🟡 Medium', '🔴 High']
    })

    # Color code rows based on priority
    def highlight_priority(row):
        if '🔴 High' in row['Priority']:
            return ['background-color: #ffe6e6'] * len(row)
        elif '🟡 Medium' in row['Priority']:
            return ['background-color: #fff4e6'] * len(row)
        else:
            return ['background-color: #e6ffe6'] * len(row)

    styled_df = deadlines.style.apply(highlight_priority, axis=1)
    st.dataframe(styled_df, use_container_width=True)

    # Schedule adjustment
    st.markdown("---")
    st.subheader("🔄 Request Extension")

    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Assignment", deadlines['Assignment'], key="student_extension_assignment")
        st.date_input("Request New Due Date", key="student_extension_date")
        st.selectbox("Reason", ["Illness", "Family Emergency", "Technical Issues", "Workload Conflict", "Other"], key="student_extension_reason")
        st.text_area("Additional Details", key="student_extension_details")
        st.button("Submit Extension Request", key="student_extension_submit")

    with col2:
        st.markdown("### Extension Policy")
        st.info("""
        **Guidelines:**
        - Requests must be submitted at least 48 hours before the deadline
        - Supporting documentation may be required
        - Maximum extension is typically 7 days
        - Each student has 3 extension tokens per semester

        **Tips:**
        - Plan ahead and communicate early
        - Be specific about your circumstances
        - Attach relevant documentation if available
        """)
        st.metric("Remaining Extension Tokens", "2 of 3", delta="-1")


def display_teacher_schedule():
    """Teacher schedule view with class management"""
    st.subheader("Class Schedule Management")

    # Class selector
    classes = ["Engineering 101", "Data Science Basics", "Advanced AI"]
    selected_class = st.selectbox("Select Class", classes, key="teacher_class_select")

    # Calendar view for teachers
    st.markdown("### Class Calendar")

    # Teacher calendar events
    teacher_events = [
        {
            "title": "📝 Quiz 1 Due",
            "start": "2025-11-08T14:00:00",
            "end": "2025-11-08T15:00:00",
            "backgroundColor": "#4ECDC4",
            "borderColor": "#4ECDC4",
        },
        {
            "title": "📊 Homework 1 Due",
            "start": "2025-11-15",
            "end": "2025-11-15",
            "backgroundColor": "#FECA57",
            "borderColor": "#FECA57",
        },
        {
            "title": "🎓 Midterm Exam",
            "start": "2025-11-20T10:00:00",
            "end": "2025-11-20T12:00:00",
            "backgroundColor": "#F38181",
            "borderColor": "#F38181",
        },
        {
            "title": "📝 Project Proposal Due",
            "start": "2025-11-25",
            "end": "2025-11-25",
            "backgroundColor": "#95E1D3",
            "borderColor": "#95E1D3",
        },
        {
            "title": "🎯 Final Exam",
            "start": "2025-12-10T09:00:00",
            "end": "2025-12-10T11:30:00",
            "backgroundColor": "#FF6B6B",
            "borderColor": "#FF6B6B",
        },
    ]

    calendar_options = {
        "editable": True,
        "selectable": True,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,listWeek",
        },
        "initialView": "dayGridMonth",
        "height": 550,
    }

    teacher_calendar = st_calendar(
        events=teacher_events,
        options=calendar_options,
        key="teacher_calendar"
    )

    # Assessment schedule table
    st.markdown("---")
    st.subheader("📅 Assessment Schedule")

    assessments = pd.DataFrame({
        'Assessment': ['Quiz 1', 'Homework 1', 'Midterm', 'Project Proposal', 'Final Exam'],
        'Type': ['Quiz', 'Assignment', 'Exam', 'Project', 'Exam'],
        'Due Date': ['Nov 8, 2025', 'Nov 15, 2025', 'Nov 20, 2025', 'Nov 25, 2025', 'Dec 10, 2025'],
        'Status': ['Open', 'Scheduled', 'Scheduled', 'Scheduled', 'Scheduled'],
        'Submissions': ['12/25', '0/25', '0/25', '0/25', '0/25']
    })

    st.dataframe(assessments, use_container_width=True)

    # Schedule management
    st.markdown("---")
    st.subheader("✏️ Modify Schedule")
    col1, col2 = st.columns(2)

    with col1:
        st.selectbox("Assessment", assessments['Assessment'], key="teacher_modify_assessment")
        st.date_input("Current Due Date", value=datetime.datetime(2025, 11, 20), key="teacher_current_date")
        st.date_input("New Due Date", key="teacher_new_date")
        st.checkbox("Notify Students", value=True, key="teacher_notify")
        st.text_area("Notification Message", key="teacher_message")
        st.button("Update Schedule", key="teacher_update_schedule")

    with col2:
        st.markdown("### 📊 Workload Analysis")
        st.info("Current schedule shows balanced workload distribution. November 20-25 has higher concentration of deadlines.")

        # Workload visualization
        weeks = [f"Week {i}" for i in range(1, 11)]
        workload = [1, 2, 1, 0, 3, 2, 1, 2, 0, 2]

        workload_data = pd.DataFrame({
            'Week': weeks,
            'Assessments': workload
        })

        st.bar_chart(workload_data.set_index('Week'))

    # Extension requests
    st.markdown("---")
    st.subheader("📬 Extension Requests")

    extension_requests = pd.DataFrame({
        'Student': ['John D.', 'Maria S.', 'Alex T.', 'Laura H.'],
        'Assignment': ['Homework 3', 'Midterm', 'Project Proposal', 'Quiz 5'],
        'Current Due': ['Nov 15, 2025', 'Nov 20, 2025', 'Nov 25, 2025', 'Nov 8, 2025'],
        'Requested Due': ['Nov 19, 2025', 'Nov 24, 2025', 'Dec 2, 2025', 'Nov 11, 2025'],
        'Reason': ['Illness', 'Family Emergency', 'Technical Issues', 'Workload Conflict'],
        'Status': ['🟡 Pending', '🟡 Pending', '🟡 Pending', '🟡 Pending']
    })

    st.dataframe(extension_requests, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("✅ Approve Selected", key="teacher_approve")
    with col2:
        st.button("❌ Deny Selected", key="teacher_deny")
    with col3:
        st.button("💬 Request More Info", key="teacher_info")
