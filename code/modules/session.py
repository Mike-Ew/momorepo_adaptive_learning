# session.py
import streamlit as st
from datetime import datetime, timedelta
import uuid

# Session configuration
SESSION_TIMEOUT = 30  # minutes


def initialize_session():
    """Initialize or update session variables"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "last_activity" not in st.session_state:
        st.session_state.last_activity = datetime.now()
    else:
        # Update last activity time
        st.session_state.last_activity = datetime.now()


def check_session_valid():
    """Check if the current session is still valid"""
    if "last_activity" not in st.session_state:
        return False

    # Check if session has timed out
    time_elapsed = datetime.now() - st.session_state.last_activity
    if time_elapsed > timedelta(minutes=SESSION_TIMEOUT):
        return False

    return True


def end_session():
    """End the current session"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
