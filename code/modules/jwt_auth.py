# jwt_auth.py
import jwt
import datetime
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY", "your-default-secret-key"
)  # Use environment variable in production


def generate_token(username, role):
    """Generate a JWT token for the user"""
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(hours=24),  # 24 hour expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def verify_token(token):
    """Verify a JWT token and return the payload if valid"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, "Token has expired"
    except jwt.InvalidTokenError:
        return False, "Invalid token"

