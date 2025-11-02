# rbac.py
import streamlit as st

# Define permissions
PERMISSIONS = {
    "admin": [
        "view_all_users",
        "create_user",
        "delete_user",
        "edit_user",
        "view_all_courses",
        "create_course",
        "delete_course",
        "edit_course",
        "view_all_analytics",
        "configure_system",
        "manage_ml_models",
    ],
    "teacher": [
        "view_own_courses",
        "edit_own_courses",
        "create_content",
        "view_student_progress",
        "provide_feedback",
        "adjust_schedules",
        "create_assessments",
        "view_class_analytics",
    ],
    "student": [
        "view_own_courses",
        "submit_assignments",
        "take_assessments",
        "view_own_progress",
        "view_recommendations",
        "adjust_own_schedule",
    ],
}


def has_permission(required_permission):
    """Check if current user has the required permission"""
    if "role" not in st.session_state:
        return False

    user_role = st.session_state.role
    user_permissions = PERMISSIONS.get(user_role, [])

    return required_permission in user_permissions


def requires_permission(permission):
    """Decorator for functions that require specific permissions"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            if has_permission(permission):
                return func(*args, **kwargs)
            else:
                st.error("You don't have permission to access this feature.")
                return None

        return wrapper

    return decorator
