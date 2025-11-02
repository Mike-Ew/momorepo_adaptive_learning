# user_management.py - User management page for admins
import streamlit as st
from modules.auth import load_users, create_user


def display_user_management():
    """Admin page for managing users"""
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
