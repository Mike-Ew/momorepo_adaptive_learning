import pandas as pd
import numpy as np


def load_student_data(source="mock"):
    """
    Load student data from various sources
    """
    if source == "mock":
        # Generate mock data for testing
        return pd.DataFrame(
            {
                "Student ID": range(1, 21),
                "Course": ["Engineering 101"] * 20,
                "Engagement Score": np.random.uniform(0.2, 0.9, 20),
                "Quiz Avg": np.random.uniform(60, 95, 20),
                "Time Spent (hrs)": np.random.uniform(5, 30, 20),
                "Risk Level": np.random.choice(
                    ["Low", "Medium", "High"], 20, p=[0.6, 0.3, 0.1]
                ),
            }
        )
    else:
        # In production, connect to your database
        # return pd.read_sql("SELECT * FROM students", connection)
        pass


def process_interaction_data(student_id):
    """
    Process student interaction data for recommendation engine
    """
    # This would extract features from clickstream data, quiz results, etc.
    # For now, return mock interaction data
    return {
        "login_frequency": np.random.randint(1, 10),
        "avg_session_duration": np.random.uniform(10, 60),
        "content_interactions": np.random.randint(20, 100),
        "quiz_attempts": np.random.randint(1, 5),
        "forum_posts": np.random.randint(0, 10),
    }
