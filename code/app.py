# app.py - Main entry point for Adaptive Learning Platform
import streamlit as st
import datetime
from modules.auth import authenticate, create_user, change_password
from modules.session import initialize_session, check_session_valid, end_session
from modules.jwt_auth import generate_token, verify_token

# Import page modules
from pages.common.dashboard import display_dashboard
from pages.admin.user_management import display_user_management
from pages.admin.system_settings import display_system_settings
from pages.teacher.class_management import display_class_management
from pages.teacher.student_progress import display_student_progress
from pages.teacher.content_management import display_content_management
from pages.teacher.analytics import display_analytics
from pages.student.learning_path import display_learning_path
from pages.student.performance import display_student_performance
from pages.student.schedule import display_schedule
from pages.student.resources import display_resources

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


def login_ui():
    """Display login and registration interface"""
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


def main_app():
    """Main application with role-based navigation"""
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

    # Page routing - dispatch to appropriate page module
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
