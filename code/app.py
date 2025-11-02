# app.py
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go
from modules.auth import authenticate, create_user, load_users, change_password, get_user_preferences, update_user_preferences
from modules.session import initialize_session, check_session_valid, end_session
from modules.rbac import requires_permission, has_permission
from modules.jwt_auth import generate_token, verify_token

# Set page configuration
st.set_page_config(
    page_title="Adaptive Learning Platform",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session
initialize_session()

# Check if session is valid
if not check_session_valid() and 'logged_in' in st.session_state and st.session_state.logged_in:
    st.warning("Your session has expired. Please log in again.")
    end_session()
    st.rerun()

# Authentication UI
def login_ui():
    st.title("Adaptive Learning Platform")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if username and password:
                success, role = authenticate(username, password)
                if success:
                    # Generate JWT token
                    token = generate_token(username, role)
                    
                    # Set session variables
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = role
                    st.session_state.token = token
                    st.session_state.last_activity = datetime.datetime.now()
                    
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter both username and password")
    
    with tab2:
        st.subheader("Register")
        new_username = st.text_input("Username", key="reg_username")
        new_password = st.text_input("Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
        email = st.text_input("Email", key="reg_email")
        role = st.selectbox("Role", ["student", "teacher"], key="reg_role")
        
        if st.button("Register"):
            if new_username and new_password and confirm_password and email:
                if new_password == confirm_password:
                    success, message = create_user(new_username, new_password, role, email)
                    if success:
                        st.success(message)
                        st.info("You can now login with your credentials")
                    else:
                        st.error(message)
                else:
                    st.error("Passwords do not match")
            else:
                st.warning("Please fill out all fields")

def logout():
    """Logout the current user"""
    end_session()
    st.rerun()

# Main application with access control
def main_app():
    # Sidebar with navigation and user info
    st.sidebar.title("Adaptive Learning Platform")
    st.sidebar.write(f"Logged in as: {st.session_state.username}")
    st.sidebar.write(f"Role: {st.session_state.role}")
    
    # Different navigation options based on role
    if st.session_state.role == "admin":
        page = st.sidebar.selectbox(
            "Navigate", 
            ["Dashboard", "User Management", "Course Management", "System Settings"]
        )
    elif st.session_state.role == "teacher":
        page = st.sidebar.selectbox(
            "Navigate", 
            ["Dashboard", "Class Management", "Student Progress", "Content Management", "Analytics"]
        )
    else:  # student
        page = st.sidebar.selectbox(
            "Navigate", 
            ["Dashboard", "My Learning Path", "Performance", "Schedule", "Resources"]
        )
    
    # Account settings and logout
    st.sidebar.markdown("---")
    if st.sidebar.expander("Account Settings"):
        old_password = st.sidebar.text_input("Current Password", type="password", key="current_pwd")
        new_password = st.sidebar.text_input("New Password", type="password", key="new_pwd")
        confirm_new = st.sidebar.text_input("Confirm New Password", type="password", key="confirm_new_pwd")
        
        if st.sidebar.button("Change Password"):
            if new_password == confirm_new:
                success, message = change_password(st.session_state.username, old_password, new_password)
                if success:
                    st.sidebar.success(message)
                else:
                    st.sidebar.error(message)
            else:
                st.sidebar.error("New passwords don't match")
    
    if st.sidebar.button("Logout"):
        logout()
    
    # Page content based on selection
    if page == "Dashboard":
        display_dashboard()
    elif page == "User Management" and st.session_state.role == "admin":
        display_user_management()
    elif page == "Class Management" and st.session_state.role == "teacher":
        display_class_management()
    elif page == "Student Progress" and st.session_state.role == "teacher":
        display_student_progress()
    elif page == "My Learning Path" and st.session_state.role == "student":
        display_learning_path()
    elif page == "Performance" and st.session_state.role == "student":
        display_student_performance()
    elif page == "Schedule":
        display_schedule()
    elif page == "Resources" and st.session_state.role == "student":
        display_resources()
    elif page == "Content Management" and st.session_state.role == "teacher":
        display_content_management()
    elif page == "Analytics" and (st.session_state.role == "teacher" or st.session_state.role == "admin"):
        display_analytics()
    elif page == "System Settings" and st.session_state.role == "admin":
        display_system_settings()
    else:
        st.error("You don't have permission to access this page")

def display_dashboard():
    st.title("Dashboard")
    
    # Different dashboard content based on role
    if st.session_state.role == "admin":
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
        
    elif st.session_state.role == "teacher":
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
        
    else:  # student
        st.header("Student Dashboard")
        
        # Progress overview
        st.subheader("Your Progress")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Overall Progress", "68%")
            st.metric("Assignments Completed", "12/20")
            
            # Progress by course
            st.subheader("Progress by Course")
            course_progress = pd.DataFrame({
                'Course': ['Engineering 101', 'Data Science Basics', 'Physics Fundamentals'],
                'Progress': [75, 62, 45]
            })
            fig = px.bar(course_progress, x='Course', y='Progress', text='Progress',
                         color='Progress', color_continuous_scale='blues')
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            st.plotly_chart(fig)
            
        with col2:
            st.markdown("### Next Deadlines")
            st.info("Assignment 3: Due in 2 days")
            st.info("Quiz 5: Due in 5 days")
            st.info("Project Milestone: Due in 1 week")
            
            # Study time
            st.subheader("Weekly Study Time")
            study_data = pd.DataFrame({
                'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'Hours': [2.5, 1.5, 3.0, 2.0, 1.0, 4.0, 2.5]
            })
            st.bar_chart(study_data.set_index('Day'))
        
        # Recommendations
        st.subheader("Personalized Recommendations")
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

def display_user_management():
    st.title("User Management")
    
    users = load_users()
    # Filter out admin from display for security
    display_users = users[users['role'] != 'admin'].copy()
    
    # Add view options
    view_option = st.radio("View", ["All Users", "Teachers", "Students"])
    
    if view_option == "Teachers":
        filtered_users = display_users[display_users['role'] == 'teacher']
    elif view_option == "Students":
        filtered_users = display_users[display_users['role'] == 'student']
    else:
        filtered_users = display_users
    
    # Add search functionality
    search_term = st.text_input("Search Users", "")
    if search_term:
        filtered_users = filtered_users[
            filtered_users['username'].str.contains(search_term, case=False) |
            filtered_users['email'].str.contains(search_term, case=False)
        ]
    
    st.dataframe(filtered_users[['username', 'role', 'email', 'last_login']])
    
    # User creation form
    with st.expander("Add New User"):
        with st.form("add_user_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            new_email = st.text_input("Email")
            new_role = st.selectbox("Role", ["teacher", "student"])
            
            submitted = st.form_submit_button("Add User")
            if submitted:
                success, message = create_user(new_username, new_password, new_role, new_email)
                if success:
                    st.success(message)
                    st.rerun()  # Refresh page to show new user
                else:
                    st.error(message)
    
    # Bulk user operations
    with st.expander("Bulk Operations"):
        st.file_uploader("Upload User CSV", type=["csv"])
        st.download_button("Download User Template", 
                          data="username,email,role,password\nuser1,user1@example.com,student,password1",
                          file_name="user_template.csv")
        st.button("Export All Users")

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

def display_learning_path():
    st.title("My Learning Path")
    
    # Overview metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Progress", "68%")
    with col2:
        st.metric("Current Module", "Module 3: Advanced Concepts")
    with col3:
        st.metric("Pace", "On Track", delta="2 days ahead")
    
    # Learning path visualization
    st.subheader("Your Learning Journey")

    # Path visualization
    modules = ["Introduction", "Basic Concepts", "Advanced Theory", "Practical Application", "Final Project"]
    progress = [100, 80, 45, 10, 0]
    status = ['Completed', 'Completed', 'In Progress', 'Not Started', 'Not Started']

    # Create DataFrame for Plotly
    journey_df = pd.DataFrame({
        'Module': modules,
        'Progress': progress,
        'Status': status
    })

    # Create color mapping based on progress
    color_map = {
        'Completed': '#28a745',      # green
        'In Progress': '#ffc107',    # orange
        'Not Started': '#6c757d'     # gray
    }

    fig = px.bar(journey_df,
                 y='Module',
                 x='Progress',
                 orientation='h',
                 color='Status',
                 color_discrete_map=color_map,
                 text='Progress',
                 labels={'Progress': 'Progress (%)'},
                 height=300)

    fig.update_traces(texttemplate='%{text}%', textposition='inside')
    fig.update_layout(
        xaxis_range=[0, 100],
        showlegend=True,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed module view
    st.subheader("Current Module: Advanced Theory")
    
    # Topics in current module
    topics = pd.DataFrame({
        'Topic': ['3.1 Complex Variables', '3.2 Matrix Operations', '3.3 Differential Equations', '3.4 Numerical Methods'],
        'Status': ['Completed', 'In Progress', 'Not Started', 'Not Started'],
        'Score': ['92%', '-', '-', '-'],
        'Recommended Focus': ['Low', 'High', 'Medium', 'Low']
    })
    
    st.dataframe(topics)
    
    # Personalized recommendations
    st.subheader("Recommended Next Steps")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### Primary Recommendation")
        st.info("Complete Matrix Operations (3.2)")
        st.button("Continue Learning", key="rec1")
    
    with col2:
        st.markdown("### Alternative Path")
        st.info("Preview Differential Equations (3.3)")
        st.button("Explore Topic", key="rec2")
    
    with col3:
        st.markdown("### Additional Practice")
        st.info("Review Basic Matrix Concepts (2.4)")
        st.button("Review Material", key="rec3")
    
    # Learning style adaptation
    st.subheader("Learning Preferences")

    # Get current user preferences from database
    username = st.session_state.get('username', '')
    user_prefs = get_user_preferences(username)

    # Show current preferences
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Current Preferences")
        if user_prefs and user_prefs['learning_style']:
            st.markdown(f"**Learning Style:** {user_prefs['learning_style']}")
            st.markdown(f"**Preferred Pace:** {user_prefs['preferred_pace']}")
            st.markdown(f"**Content Format:** {user_prefs['content_format']}")
        else:
            st.info("No learning preferences set. Take the assessment to personalize your experience!")

    with col2:
        st.markdown("### Update Preferences")
        if st.button("Update Learning Preferences", key="update_prefs_btn"):
            st.session_state.show_preferences_form = True
        if st.button("Take Learning Style Assessment", key="take_assessment_btn"):
            st.session_state.show_assessment = True

    # Radar chart visualization of learning style
    if user_prefs and user_prefs['learning_style']:
        st.markdown("---")
        st.subheader("Your Learning Profile")

        # Map learning style to scores for radar chart
        learning_style_scores = {
            "Visual/Interactive": {"Visual": 90, "Reading": 40, "Auditory": 50, "Kinesthetic": 70},
            "Reading/Text": {"Visual": 40, "Reading": 95, "Auditory": 30, "Kinesthetic": 35},
            "Auditory/Visual": {"Visual": 75, "Reading": 45, "Auditory": 90, "Kinesthetic": 40},
            "Kinesthetic/Hands-on": {"Visual": 55, "Reading": 35, "Auditory": 40, "Kinesthetic": 95},
            "Mixed": {"Visual": 70, "Reading": 70, "Auditory": 70, "Kinesthetic": 70}
        }

        # Get scores for current learning style
        current_style = user_prefs['learning_style']
        scores = learning_style_scores.get(current_style, {"Visual": 50, "Reading": 50, "Auditory": 50, "Kinesthetic": 50})

        # Create radar chart data
        categories = list(scores.keys())
        values = list(scores.values())

        # Create the radar chart using plotly
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=current_style,
            fillcolor='rgba(99, 110, 250, 0.4)',
            line=dict(color='rgba(99, 110, 250, 1)', width=2)
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickmode='linear',
                    tick0=0,
                    dtick=25,
                    gridcolor='lightgray'
                ),
                angularaxis=dict(
                    gridcolor='lightgray'
                )
            ),
            showlegend=True,
            title=dict(
                text=f"Learning Style Profile: {current_style}",
                x=0.5,
                xanchor='center'
            ),
            height=450,
            margin=dict(l=80, r=80, t=80, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)

    # Show preferences update form
    if st.session_state.get('show_preferences_form', False):
        st.markdown("---")
        st.subheader("Update Your Learning Preferences")

        with st.form("learning_preferences_form"):
            col1, col2, col3 = st.columns(3)

            with col1:
                learning_style = st.selectbox(
                    "Learning Style",
                    ["Visual/Interactive", "Reading/Text", "Auditory/Visual", "Kinesthetic/Hands-on", "Mixed"],
                    index=0 if not user_prefs or not user_prefs['learning_style'] else
                          ["Visual/Interactive", "Reading/Text", "Auditory/Visual", "Kinesthetic/Hands-on", "Mixed"].index(user_prefs['learning_style'])
                          if user_prefs['learning_style'] in ["Visual/Interactive", "Reading/Text", "Auditory/Visual", "Kinesthetic/Hands-on", "Mixed"] else 0,
                    key="pref_learning_style"
                )

            with col2:
                preferred_pace = st.selectbox(
                    "Preferred Pace",
                    ["Slow", "Moderate", "Fast", "Self-paced"],
                    index=1 if not user_prefs or not user_prefs['preferred_pace'] else
                          ["Slow", "Moderate", "Fast", "Self-paced"].index(user_prefs['preferred_pace'])
                          if user_prefs['preferred_pace'] in ["Slow", "Moderate", "Fast", "Self-paced"] else 1,
                    key="pref_pace"
                )

            with col3:
                content_format = st.selectbox(
                    "Content Format",
                    ["Videos + Quizzes", "Articles + Quizzes", "Video + Practice Problems",
                     "Interactive Simulations", "Videos + Discussions", "Mixed Content"],
                    index=2 if not user_prefs or not user_prefs['content_format'] else
                          ["Videos + Quizzes", "Articles + Quizzes", "Video + Practice Problems",
                           "Interactive Simulations", "Videos + Discussions", "Mixed Content"].index(user_prefs['content_format'])
                          if user_prefs['content_format'] in ["Videos + Quizzes", "Articles + Quizzes", "Video + Practice Problems",
                                                               "Interactive Simulations", "Videos + Discussions", "Mixed Content"] else 2,
                    key="pref_content_format"
                )

            col1, col2 = st.columns([1, 4])
            with col1:
                submitted = st.form_submit_button("Save Preferences")
            with col2:
                cancel = st.form_submit_button("Cancel")

            if submitted:
                success, message = update_user_preferences(
                    username,
                    learning_style=learning_style,
                    preferred_pace=preferred_pace,
                    content_format=content_format
                )
                if success:
                    st.success(message)
                    st.session_state.show_preferences_form = False
                    st.rerun()
                else:
                    st.error(message)

            if cancel:
                st.session_state.show_preferences_form = False
                st.rerun()

    # Show learning style assessment
    if st.session_state.get('show_assessment', False):
        st.markdown("---")
        st.subheader("Learning Style Assessment")
        st.info("Answer these questions to help us understand how you learn best!")

        with st.form("learning_assessment_form"):
            st.markdown("#### 1. How do you prefer to receive new information?")
            q1 = st.radio(
                "Select one:",
                ["Through videos and visual demonstrations",
                 "By reading articles and textbooks",
                 "Through listening to lectures and discussions",
                 "By doing hands-on activities and experiments"],
                key="assessment_q1"
            )

            st.markdown("#### 2. What's your ideal study environment?")
            q2 = st.radio(
                "Select one:",
                ["Watching tutorial videos at my own pace",
                 "Reading detailed documentation and notes",
                 "Group discussions and study sessions",
                 "Working on practice problems and projects"],
                key="assessment_q2"
            )

            st.markdown("#### 3. How quickly do you like to progress through material?")
            q3 = st.radio(
                "Select one:",
                ["I prefer to take my time and go slowly",
                 "A moderate, steady pace works best for me",
                 "I like to move quickly through material",
                 "I prefer complete flexibility in my pacing"],
                key="assessment_q3"
            )

            st.markdown("#### 4. What helps you retain information best?")
            q4 = st.radio(
                "Select one:",
                ["Visual diagrams and videos",
                 "Written summaries and notes",
                 "Discussion and repetition",
                 "Practical application and practice"],
                key="assessment_q4"
            )

            col1, col2 = st.columns([1, 4])
            with col1:
                assess_submitted = st.form_submit_button("Submit Assessment")
            with col2:
                assess_cancel = st.form_submit_button("Cancel")

            if assess_submitted:
                # Determine learning style based on answers
                visual_score = (1 if "videos" in q1.lower() else 0) + (1 if "videos" in q2.lower() else 0) + (1 if "Visual" in q4 else 0)
                reading_score = (1 if "reading" in q1.lower() else 0) + (1 if "Reading" in q2.lower() else 0) + (1 if "Written" in q4 else 0)
                auditory_score = (1 if "listening" in q1.lower() else 0) + (1 if "discussions" in q2.lower() else 0) + (1 if "Discussion" in q4 else 0)
                kinesthetic_score = (1 if "hands-on" in q1.lower() else 0) + (1 if "practice" in q2.lower() else 0) + (1 if "Practical" in q4 else 0)

                # Determine primary learning style
                scores = {
                    "Visual/Interactive": visual_score,
                    "Reading/Text": reading_score,
                    "Auditory/Visual": auditory_score,
                    "Kinesthetic/Hands-on": kinesthetic_score
                }
                primary_style = max(scores, key=scores.get)

                # Determine pace
                pace_map = {
                    "I prefer to take my time and go slowly": "Slow",
                    "A moderate, steady pace works best for me": "Moderate",
                    "I like to move quickly through material": "Fast",
                    "I prefer complete flexibility in my pacing": "Self-paced"
                }
                pace = pace_map[q3]

                # Determine content format
                if primary_style == "Visual/Interactive":
                    content = "Video + Practice Problems"
                elif primary_style == "Reading/Text":
                    content = "Articles + Quizzes"
                elif primary_style == "Auditory/Visual":
                    content = "Videos + Discussions"
                else:
                    content = "Interactive Simulations"

                # Save preferences
                success, message = update_user_preferences(
                    username,
                    learning_style=primary_style,
                    preferred_pace=pace,
                    content_format=content
                )

                if success:
                    st.success(f"✅ Assessment complete! Your learning style is: **{primary_style}**")
                    st.info(f"Based on your responses, we recommend: {content} at a {pace} pace.")
                    st.session_state.show_assessment = False
                    st.balloons()
                    st.rerun()
                else:
                    st.error(message)

            if assess_cancel:
                st.session_state.show_assessment = False
                st.rerun()

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

def display_student_progress():
    st.title("Student Progress Monitoring")
    
    # Class selector
    classes = ["Engineering 101", "Data Science Basics", "Advanced AI"]
    selected_class = st.selectbox("Select Class", classes)
    
    # Overview metrics
    st.subheader(f"{selected_class} Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Class Average", "76%")
    with col2:
        st.metric("Completion Rate", "68%")
    with col3:
        st.metric("At-Risk Students", "4", delta="-2")
    with col4:
        st.metric("Engagement Score", "Medium")
    
    # Learning Style Distribution for the class
    st.subheader("Class Learning Style Distribution")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Mock class learning style data (in production, aggregate from all students)
        learning_styles_count = {
            "Visual/Interactive": 10,
            "Reading/Text": 6,
            "Auditory/Visual": 5,
            "Kinesthetic/Hands-on": 3,
            "Mixed": 1
        }

        # Create pie chart
        fig_pie = px.pie(
            values=list(learning_styles_count.values()),
            names=list(learning_styles_count.keys()),
            title="Learning Style Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown("### Class Insights")
        st.metric("Most Common Style", "Visual/Interactive", "40%")
        st.metric("Least Common Style", "Mixed", "4%")

        st.markdown("### Teaching Strategy")
        st.info("""
        **Recommendations for this class:**

        • Prioritize visual content (videos, diagrams)

        • Provide text alternatives for readers

        • Include discussion opportunities

        • Offer varied content formats
        """)

    # Average class learning profile radar chart
    st.subheader("Average Class Learning Profile")

    # Calculate average scores across all learning styles in the class
    avg_scores = {"Visual": 0, "Reading": 0, "Auditory": 0, "Kinesthetic": 0}

    learning_style_scores = {
        "Visual/Interactive": {"Visual": 90, "Reading": 40, "Auditory": 50, "Kinesthetic": 70},
        "Reading/Text": {"Visual": 40, "Reading": 95, "Auditory": 30, "Kinesthetic": 35},
        "Auditory/Visual": {"Visual": 75, "Reading": 45, "Auditory": 90, "Kinesthetic": 40},
        "Kinesthetic/Hands-on": {"Visual": 55, "Reading": 35, "Auditory": 40, "Kinesthetic": 95},
        "Mixed": {"Visual": 70, "Reading": 70, "Auditory": 70, "Kinesthetic": 70}
    }

    # Calculate weighted average based on distribution
    total_students = sum(learning_styles_count.values())
    for style, count in learning_styles_count.items():
        weight = count / total_students
        style_scores = learning_style_scores[style]
        for dimension in avg_scores:
            avg_scores[dimension] += style_scores[dimension] * weight

    categories = list(avg_scores.keys())
    values = list(avg_scores.values())

    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Class Average',
        fillcolor='rgba(46, 204, 113, 0.4)',
        line=dict(color='rgba(46, 204, 113, 1)', width=2)
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickmode='linear',
                tick0=0,
                dtick=25,
                gridcolor='lightgray'
            ),
            angularaxis=dict(
                gridcolor='lightgray'
            )
        ),
        showlegend=True,
        title=dict(
            text="Class Average Learning Profile",
            x=0.5,
            xanchor='center'
        ),
        height=400,
        margin=dict(l=60, r=60, t=60, b=40)
    )

    st.plotly_chart(fig_radar, use_container_width=True)

    # Progress distribution
    st.markdown("---")
    st.subheader("Progress Distribution")

    # Mock progress data
    progress_ranges = ['0-25%', '26-50%', '51-75%', '76-100%']
    student_counts = [2, 5, 10, 8]

    fig = px.bar(
        x=progress_ranges,
        y=student_counts,
        labels={'x': 'Progress Range', 'y': 'Number of Students'},
        color=student_counts,
        color_continuous_scale='blues'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Student list with risk levels
    st.subheader("Student List")
    
    # Add filters
    col1, col2, col3 = st.columns(3)
    with col1:
        risk_filter = st.multiselect("Risk Level", ["High", "Medium", "Low"], default=[])
    with col2:
        progress_filter = st.slider("Progress Range", 0, 100, (0, 100))
    with col3:
        sort_by = st.selectbox("Sort By", ["Risk (High to Low)", "Progress (Low to High)", "Name"])
    
    # Mock student data
    students = pd.DataFrame({
        'Student ID': range(1001, 1026),
        'Name': [f"Student {i}" for i in range(1, 26)],
        'Progress': np.random.uniform(20, 95, 25),
        'Last Active': [f"{i} days ago" for i in np.random.randint(1, 10, 25)],
        'Risk Level': np.random.choice(['Low', 'Medium', 'High'], 25, p=[0.7, 0.2, 0.1]),
        'Action Needed': np.random.choice(['None', 'Check-in', 'Intervention'], 25, p=[0.6, 0.3, 0.1])
    })
    
    # Apply filters
    if risk_filter:
        students = students[students['Risk Level'].isin(risk_filter)]
    
    students = students[(students['Progress'] >= progress_filter[0]) & 
                       (students['Progress'] <= progress_filter[1])]
    
    # Apply sorting
    if sort_by == "Risk (High to Low)":
        risk_order = {'High': 0, 'Medium': 1, 'Low': 2}
        students['Risk Order'] = students['Risk Level'].map(risk_order)
        students = students.sort_values('Risk Order')
        students = students.drop('Risk Order', axis=1)
    elif sort_by == "Progress (Low to High)":
        students = students.sort_values('Progress')
    else:  # Name
        students = students.sort_values('Name')
    
    # Format progress as percentage
    students['Progress'] = students['Progress'].apply(lambda x: f"{x:.1f}%")
    
    # Display student table
    st.dataframe(students)
    
    # Individual student analysis
    st.subheader("Individual Student Analysis")

    selected_student = st.selectbox("Select Student", students['Name'], key="individual_student_select")

    col1, col2 = st.columns(2)
    with col1:
        # Mock individual student data
        st.markdown(f"### {selected_student}")
        st.markdown("**Progress:** 67.5%")
        st.markdown("**Risk Level:** Medium")
        st.markdown("**Last Active:** 2 days ago")
        st.markdown("**Learning Style:** Visual/Interactive")
        st.markdown("**Preferred Pace:** Moderate")
        st.markdown("**Content Format:** Video + Practice Problems")
        st.markdown("**Engagement Pattern:** Sporadic")

        # Actions
        st.button("Send Message", key="teacher_send_msg")
        st.button("Adjust Schedule", key="teacher_adjust_schedule")
        st.button("Provide Resources", key="teacher_provide_resources")

    with col2:
        # Activity timeline
        st.markdown("### Recent Activity")
        activities = [
            "Completed Quiz 3 (Score: 75%)",
            "Viewed Lecture 5",
            "Submitted Assignment 2 (Late)",
            "Started Topic 3.2",
            "Posted in Discussion Forum"
        ]
        activity_dates = [
            "2 days ago",
            "2 days ago",
            "5 days ago",
            "1 week ago",
            "1 week ago"
        ]

        for i in range(len(activities)):
            st.markdown(f"**{activity_dates[i]}:** {activities[i]}")

    # Learning style visualization for individual student
    st.markdown("---")
    st.subheader(f"{selected_student}'s Learning Profile")

    # Mock learning style for demonstration (in production, fetch from user data)
    student_learning_style = "Visual/Interactive"  # This would come from get_user_preferences()

    learning_style_scores = {
        "Visual/Interactive": {"Visual": 90, "Reading": 40, "Auditory": 50, "Kinesthetic": 70},
        "Reading/Text": {"Visual": 40, "Reading": 95, "Auditory": 30, "Kinesthetic": 35},
        "Auditory/Visual": {"Visual": 75, "Reading": 45, "Auditory": 90, "Kinesthetic": 40},
        "Kinesthetic/Hands-on": {"Visual": 55, "Reading": 35, "Auditory": 40, "Kinesthetic": 95},
        "Mixed": {"Visual": 70, "Reading": 70, "Auditory": 70, "Kinesthetic": 70}
    }

    scores = learning_style_scores.get(student_learning_style, {"Visual": 50, "Reading": 50, "Auditory": 50, "Kinesthetic": 50})

    col1, col2 = st.columns([2, 1])

    with col1:
        # Create radar chart
        categories = list(scores.keys())
        values = list(scores.values())

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=student_learning_style,
            fillcolor='rgba(99, 110, 250, 0.4)',
            line=dict(color='rgba(99, 110, 250, 1)', width=2)
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickmode='linear',
                    tick0=0,
                    dtick=25,
                    gridcolor='lightgray'
                ),
                angularaxis=dict(
                    gridcolor='lightgray'
                )
            ),
            showlegend=True,
            title=dict(
                text=f"Learning Style: {student_learning_style}",
                x=0.5,
                xanchor='center'
            ),
            height=400,
            margin=dict(l=60, r=60, t=60, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Teaching Recommendations")
        st.info("""
        **Based on this student's learning profile:**

        ✓ Emphasize visual materials and diagrams

        ✓ Include hands-on practice exercises

        ✓ Use video tutorials when possible

        ✓ Provide interactive simulations

        ✓ Limit text-heavy readings
        """)

        st.markdown("### Content Preferences")
        st.success("**Best Format:** Video + Practice Problems")
        st.success("**Preferred Pace:** Moderate")

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

def display_analytics():
    st.title("Learning Analytics")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.role == "admin":
            course_options = ["All Courses", "Engineering 101", "Data Science Basics", "Advanced AI"]
        else:  # teacher
            course_options = ["Engineering 101", "Data Science Basics", "Advanced AI"]
        
        selected_course = st.selectbox("Course", course_options)
    
    with col2:
        time_period = st.selectbox("Time Period", ["Last Week", "Last Month", "This Semester", "All Time"])
    
    with col3:
        metric_focus = st.selectbox("Metric Focus", ["Engagement", "Performance", "Risk", "Content Effectiveness"])
    
    # Overview metrics
    st.subheader("Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Engagement Score", "76%", delta="3%")
    with col2:
        st.metric("Average Performance", "82%", delta="-1%")
    with col3:
        st.metric("At-Risk Students", "15%", delta="-2%")
    with col4:
        st.metric("Content Effectiveness", "Medium")
    
    # Main analytics based on selected focus
    if metric_focus == "Engagement":
        st.subheader("Engagement Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Engagement Over Time")
            # Mock engagement data
            dates = pd.date_range(start='2025-01-01', periods=10, freq='W')
            engagement = [68, 72, 75, 73, 76, 79, 78, 82, 80, 76]
            
            engagement_data = pd.DataFrame({
                'Date': dates,
                'Engagement': engagement
            })
            
            st.line_chart(engagement_data.set_index('Date'))
        
        with col2:
            st.markdown("### Engagement by Activity Type")
            
            activity_types = ['Video Lectures', 'Readings', 'Discussions', 'Practice Problems', 'Assessments']
            activity_scores = [85, 65, 72, 80, 78]
            
            activity_data = pd.DataFrame({
                'Activity': activity_types,
                'Engagement': activity_scores
            })
            
            fig = px.bar(
                activity_data, 
                y='Activity', 
                x='Engagement', 
                orientation='h',
                color='Engagement',
                color_continuous_scale='blues'
            )
            
            st.plotly_chart(fig)
        
        # Engagement patterns
        st.subheader("Engagement Patterns")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Time of Day Activity")
            
            hours = list(range(24))
            activity = [5, 3, 1, 0, 0, 2, 8, 15, 25, 28, 20, 18, 22, 25, 28, 30, 25, 18, 15, 12, 10, 8, 7, 6]
            
            time_data = pd.DataFrame({
                'Hour': [f"{h:02d}:00" for h in hours],
                'Activity': activity
            })
            
            st.bar_chart(time_data.set_index('Hour'))
        
        with col2:
            st.markdown("### Day of Week Activity")
            
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_activity = [85, 82, 78, 75, 65, 45, 55]
            
            day_data = pd.DataFrame({
                'Day': days,
                'Activity': day_activity
            })
            
            st.bar_chart(day_data.set_index('Day'))
    
    elif metric_focus == "Performance":
        st.subheader("Performance Analytics")
        
        # Grade distribution
        st.markdown("### Grade Distribution")
        
        grade_ranges = ['90-100%', '80-89%', '70-79%', '60-69%', 'Below 60%']
        student_counts = [15, 25, 35, 18, 7]
        
        grade_data = pd.DataFrame({
            'Grade Range': grade_ranges,
            'Student Count': student_counts
        })
        
        fig = px.bar(
            grade_data,
            x='Grade Range',
            y='Student Count',
            color='Student Count',
            color_continuous_scale='blues',
            text='Student Count'
        )
        fig.update_traces(textposition='outside')
        
        st.plotly_chart(fig)
        
        # Performance by assessment type
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Performance by Assessment Type")
            
            assessment_types = ['Quizzes', 'Homework', 'Projects', 'Exams']
            performance = [78, 82, 75, 70]
            
            assessment_data = pd.DataFrame({
                'Type': assessment_types,
                'Average Score': performance
            })
            
            st.bar_chart(assessment_data.set_index('Type'))
        
        with col2:
            st.markdown("### Performance by Topic")
            
            topics = ['Topic 1', 'Topic 2', 'Topic 3', 'Topic 4', 'Topic 5']
            topic_scores = [85, 78, 65, 72, 80]
            
            topic_data = pd.DataFrame({
                'Topic': topics,
                'Average Score': topic_scores
            })
            
            st.bar_chart(topic_data.set_index('Topic'))
        
        # Detailed assessment performance
        st.markdown("### Assessment Performance Details")
        
        assessments = pd.DataFrame({
            'Assessment': ['Quiz 1', 'Homework 1', 'Quiz 2', 'Project 1', 'Midterm', 'Quiz 3'],
            'Average': [78, 82, 75, 85, 72, 80],
            'Median': [80, 85, 78, 88, 75, 82],
            'Highest': [95, 98, 92, 100, 90, 96],
            'Lowest': [45, 55, 40, 60, 38, 52],
            'Std Dev': [12, 10, 15, 11, 14, 12]
        })
        
        st.dataframe(assessments)
    
    elif metric_focus == "Risk":
        st.subheader("Risk Analytics")
        
        # Risk distribution
        st.markdown("### Student Risk Distribution")
        
        risk_levels = ['Low Risk', 'Moderate Risk', 'High Risk', 'Severe Risk']
        risk_counts = [65, 20, 10, 5]
        
        risk_data = pd.DataFrame({
            'Risk Level': risk_levels,
            'Student Count': risk_counts
        })
        
        fig = px.pie(
            risk_data,
            values='Student Count',
            names='Risk Level',
            color='Risk Level',
            color_discrete_map={
                'Low Risk': 'green',
                'Moderate Risk': 'yellow',
                'High Risk': 'orange',
                'Severe Risk': 'red'
            }
        )
        
        st.plotly_chart(fig)
        
        # Risk factors
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Primary Risk Factors")
            
            risk_factors = [
                'Low Engagement',
                'Missing Assignments',
                'Poor Quiz Performance',
                'Infrequent Logins',
                'Limited Resource Access'
            ]
            
            factor_impact = [35, 25, 20, 15, 5]
            
            factor_data = pd.DataFrame({
                'Factor': risk_factors,
                'Impact': factor_impact
            })
            
            fig = px.bar(
                factor_data,
                y='Factor',
                x='Impact',
                orientation='h',
                color='Impact',
                color_continuous_scale='reds'
            )
            
            st.plotly_chart(fig)
        
        with col2:
            st.markdown("### Risk Trend")
            
            weeks = [f"Week {i}" for i in range(1, 11)]
            high_risk = [8, 7, 9, 12, 15, 14, 12, 10, 12, 15]
            
            risk_trend = pd.DataFrame({
                'Week': weeks,
                'High Risk Students': high_risk
            })
            
            st.line_chart(risk_trend.set_index('Week'))
        
        # Intervention effectiveness
        st.markdown("### Intervention Effectiveness")
        
        interventions = pd.DataFrame({
            'Intervention Type': ['Automated Reminders', 'Personalized Resources', 'Instructor Outreach', 'Deadline Extensions', 'Study Groups'],
            'Implementation Rate': [95, 75, 60, 45, 30],
            'Success Rate': [65, 80, 85, 70, 75],
            'Average Risk Reduction': ['15%', '25%', '35%', '20%', '22%']
        })
        
        st.dataframe(interventions)
    
    elif metric_focus == "Content Effectiveness":
        st.subheader("Content Effectiveness Analytics")
        
        # Content engagement
        st.markdown("### Content Engagement Rates")
        
        content_types = ['Video Lectures', 'Readings', 'Interactive Simulations', 'Practice Problems', 'Discussion Forums']
        completion_rates = [75, 62, 88, 70, 45]
        avg_time = [25, 35, 20, 40, 15]
        
        content_data = pd.DataFrame({
            'Content Type': content_types,
            'Completion Rate': completion_rates,
            'Avg. Time (min)': avg_time
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                content_data,
                x='Content Type',
                y='Completion Rate',
                color='Completion Rate',
                color_continuous_scale='blues',
                text='Completion Rate'
            )
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            
            st.plotly_chart(fig)
        
        with col2:
            fig = px.bar(
                content_data,
                x='Content Type',
                y='Avg. Time (min)',
                color='Avg. Time (min)',
                color_continuous_scale='viridis',
                text='Avg. Time (min)'
            )
            fig.update_traces(textposition='outside')
            
            st.plotly_chart(fig)
        
        # Content effectiveness by module
        st.markdown("### Content Effectiveness by Module")
        
        modules = ['Module 1', 'Module 2', 'Module 3', 'Module 4', 'Module 5']
        effectiveness = [85, 75, 65, 80, 70]
        complexity = [25, 45, 75, 60, 80]
        
        module_data = pd.DataFrame({
            'Module': modules,
            'Effectiveness': effectiveness,
            'Complexity': complexity
        })
        
        fig = px.scatter(
            module_data,
            x='Complexity',
            y='Effectiveness',
            text='Module',
            size=[40] * len(modules),
            color='Effectiveness',
            color_continuous_scale='blues'
        )
        
        st.plotly_chart(fig)
        
        # Content improvement recommendations
        st.markdown("### Content Improvement Recommendations")
        
        recommendations = pd.DataFrame({
            'Content Item': ['Video 2.3', 'Reading 3.1', 'Quiz 2', 'Simulation 1.2', 'Homework 3'],
            'Current Effectiveness': ['Low', 'Medium', 'Low', 'Medium', 'Low'],
            'Issue': ['Too long', 'Too complex', 'Unclear questions', 'Technical issues', 'Misaligned difficulty'],
            'Recommendation': ['Split into smaller segments', 'Add supporting materials', 'Revise questions', 'Fix loading issues', 'Adjust difficulty level']
        })
        
        st.dataframe(recommendations)

def display_system_settings():
    st.title("System Settings")
    
    # System settings tabs
    tab1, tab2, tab3, tab4 = st.tabs(["General", "AI Configuration", "Integration", "Backup & Maintenance"])
    
    with tab1:
        st.subheader("General Settings")
        
        st.markdown("### Application Configuration")
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Platform Name", value="Adaptive Learning Platform")
            st.selectbox("Default Language", ["English", "Spanish", "French", "German", "Chinese"])
            st.selectbox("Time Zone", ["UTC", "US/Eastern", "US/Central", "US/Pacific", "Europe/London"])
            st.number_input("Session Timeout (minutes)", value=30)
        
        with col2:
            st.checkbox("Enable Multi-factor Authentication", value=True)
            st.checkbox("Allow Self-registration", value=True)
            st.checkbox("Enable Notifications", value=True)
            st.checkbox("Enable Analytics", value=True)
        
        st.markdown("### Email Configuration")
        st.text_input("SMTP Server")
        st.text_input("SMTP Port")
        st.text_input("Email Username")
        st.text_input("Email Password", type="password")
        st.text_input("Sender Email")
        st.checkbox("Enable SSL/TLS", value=True)
        
        st.button("Save General Settings")
    
    with tab2:
        st.subheader("AI Configuration")
        
        st.markdown("### Recommendation Engine")
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Algorithm Type", ["Multi-armed Bandit", "Collaborative Filtering", "Content-based Filtering", "Hybrid"])
            st.slider("Exploration Rate", 0.0, 1.0, 0.2)
            st.number_input("Minimum Data Points Required", value=10)
            st.checkbox("Allow Real-time Updates", value=True)
        
        with col2:
            st.multiselect("Features to Consider", 
                          ["Quiz Performance", "Assignment Completion", "Time Spent", "Learning Style", "Previous Course Performance"],
                          default=["Quiz Performance", "Assignment Completion", "Time Spent"])
            st.slider("Performance Weight", 0.0, 1.0, 0.7)
            st.slider("Engagement Weight", 0.0, 1.0, 0.3)
        
        st.markdown("### Risk Detection Model")
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Model Type", ["Random Forest", "Gradient Boosting", "Neural Network", "Logistic Regression"])
            st.slider("Detection Sensitivity", 0.0, 1.0, 0.6)
            st.number_input("Retraining Frequency (days)", value=7)
        
        with col2:
            st.multiselect("Risk Indicators", 
                          ["Low Engagement", "Missing Assignments", "Poor Performance", "Declining Trends", "Infrequent Logins"],
                          default=["Low Engagement", "Missing Assignments", "Poor Performance"])
            st.slider("False Positive Tolerance", 0.0, 1.0, 0.2)
        
        st.markdown("### Model Monitoring")
        st.checkbox("Enable Performance Logging", value=True)
        st.checkbox("Enable Automated Retraining", value=True)
        st.checkbox("Send Alert on Performance Degradation", value=True)
        
        st.button("Save AI Settings")
    
    with tab3:
        st.subheader("Integration Settings")
        
        st.markdown("### LMS Integration")
        st.selectbox("LMS Type", ["Canvas", "Moodle", "Blackboard", "D2L Brightspace", "Custom"])
        st.text_input("API Endpoint")
        st.text_input("API Key", type="password")
        st.selectbox("Sync Frequency", ["Hourly", "Daily", "Weekly"])
        st.checkbox("Two-way Sync", value=True)
        
        st.markdown("### Authentication Integration")
        st.checkbox("Enable Single Sign-On (SSO)", value=False)
        st.selectbox("SSO Provider", ["None", "Google", "Microsoft", "Okta", "SAML"])
        st.text_input("SSO Endpoint")
        st.text_input("Client ID")
        st.text_input("Client Secret", type="password")
        
        st.markdown("### Analytics Integration")
        st.checkbox("Enable Google Analytics", value=False)
        st.text_input("Google Analytics ID")
        st.checkbox("Enable Custom Analytics", value=True)
        st.text_input("Analytics Endpoint")
        
        st.button("Save Integration Settings")
    
    with tab4:
        st.subheader("Backup & Maintenance")
        
        st.markdown("### Automated Backups")
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Enable Automated Backups", value=True)
            st.selectbox("Backup Frequency", ["Daily", "Weekly", "Monthly"])
            st.number_input("Retention Period (days)", value=30)
        
        with col2:
            st.text_input("Backup Location")
            st.checkbox("Enable Encryption", value=True)
            st.checkbox("Enable Compression", value=True)
        
        st.markdown("### System Maintenance")
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Enable Maintenance Mode", value=False)
            st.date_input("Scheduled Maintenance Date")
            st.time_input("Scheduled Maintenance Time")
        
        with col2:
            st.text_area("Maintenance Message", "System will be undergoing scheduled maintenance...")
            st.number_input("Estimated Downtime (hours)", value=2)
        
        st.markdown("### System Logs")
        st.selectbox("Log Level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        st.number_input("Log Retention (days)", value=14)
        st.button("Download System Logs")
        
        st.button("Save Maintenance Settings")

# Main logic with session validation
if __name__ == "__main__":
    # Check for authenticated session
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        # Verify JWT token
        if 'token' in st.session_state:
            valid, payload = verify_token(st.session_state.token)
            if valid:
                main_app()
            else:
                st.error("Your session is invalid. Please log in again.")
                end_session()
                st.rerun()
        else:
            main_app()  # Fallback to session-based auth if no token exists
    else:
        login_ui()