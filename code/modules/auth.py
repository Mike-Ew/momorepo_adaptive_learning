# auth.py
import streamlit as st
import pandas as pd
import hashlib
import os
from datetime import datetime, timedelta

# Get the data directory path relative to this module
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
USERS_CSV = os.path.join(DATA_DIR, "users.csv")


# Set up database connection (using CSV for simplicity, use SQL in production)
def load_users():
    if not os.path.exists(USERS_CSV):
        # Create default admin user if file doesn't exist
        users = pd.DataFrame(
            {
                "username": ["admin"],
                "password": [hashlib.sha256("admin123".encode()).hexdigest()],
                "role": ["admin"],
                "email": ["admin@example.com"],
                "last_login": [None],
                "learning_preference": [None],
                "preferred_pace": [None],
                "content_format": [None],
            }
        )
        os.makedirs(DATA_DIR, exist_ok=True)
        users.to_csv(USERS_CSV, index=False)
    else:
        users = pd.read_csv(USERS_CSV)
        # Add learning preference columns if they don't exist (for backward compatibility)
        if "learning_preference" not in users.columns:
            if "learning_style" in users.columns:
                users["learning_preference"] = users["learning_style"]
                users = users.drop(columns=["learning_style"])
            else:
                users["learning_preference"] = None
        if "preferred_pace" not in users.columns:
            users["preferred_pace"] = None
        if "content_format" not in users.columns:
            users["content_format"] = None
    return users


def save_users(users_df):
    users_df.to_csv(USERS_CSV, index=False)


def authenticate(username, password):
    users = load_users()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user_row = users[users["username"] == username]
    if not user_row.empty and user_row.iloc[0]["password"] == hashed_password:
        # Update last login
        users.loc[users["username"] == username, "last_login"] = (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        save_users(users)
        return True, user_row.iloc[0]["role"]
    return False, None


def create_user(username, password, role, email):
    users = load_users()

    # Check if username exists
    if username in users["username"].values:
        return False, "Username already exists"

    # Add new user
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    new_user = pd.DataFrame(
        {
            "username": [username],
            "password": [hashed_password],
            "role": [role],
            "email": [email],
            "last_login": [None],
            "learning_preference": [None],
            "preferred_pace": [None],
            "content_format": [None],
        }
    )

    users = pd.concat([users, new_user], ignore_index=True)
    save_users(users)
    return True, "User created successfully"


def change_password(username, current_password, new_password):
    users = load_users()
    hashed_current = hashlib.sha256(current_password.encode()).hexdigest()

    user_row = users[users["username"] == username]
    if not user_row.empty and user_row.iloc[0]["password"] == hashed_current:
        hashed_new = hashlib.sha256(new_password.encode()).hexdigest()
        users.loc[users["username"] == username, "password"] = hashed_new
        save_users(users)
        return True, "Password changed successfully"
    return False, "Current password is incorrect"


def is_authenticated():
    return "logged_in" in st.session_state and st.session_state.logged_in


def get_user_preferences(username):
    """Get learning preferences for a specific user"""
    users = load_users()
    user_row = users[users["username"] == username]

    if not user_row.empty:
        return {
            "learning_preference": user_row.iloc[0].get("learning_preference"),
            "preferred_pace": user_row.iloc[0].get("preferred_pace"),
            "content_format": user_row.iloc[0].get("content_format"),
        }
    return None


def update_user_preferences(username, learning_preference=None, preferred_pace=None, content_format=None):
    """Update learning preferences for a specific user"""
    users = load_users()

    if username not in users["username"].values:
        return False, "User not found"

    # Update only the provided fields
    if learning_preference is not None:
        users.loc[users["username"] == username, "learning_preference"] = learning_preference
    if preferred_pace is not None:
        users.loc[users["username"] == username, "preferred_pace"] = preferred_pace
    if content_format is not None:
        users.loc[users["username"] == username, "content_format"] = content_format

    save_users(users)
    return True, "Learning preferences updated successfully"
