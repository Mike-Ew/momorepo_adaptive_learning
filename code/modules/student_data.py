"""
Shared student data module
Provides consistent student profiles across teacher and student views
"""

# Define the 3 real student accounts with varied learning profiles
REAL_STUDENTS = {
    'student1': {
        'id': 1001,
        'username': 'student1',
        'name': 'Alex Johnson',
        'email': 'student1@example.com',
        'learning_style': 'Visual/Interactive',
        'preferred_pace': 'Moderate',
        'content_format': 'Video + Practice Problems',
        'overall_progress': 68,
        'current_module': 'Module 3: Advanced Theory',
        'pace_status': 'On Track',
        'pace_delta': '2 days ahead',
        'last_active': '1 day ago',
        'risk_level': 'Low',
        'action_needed': 'None',
        'engagement_pattern': 'Consistent',
        # Dashboard data
        'assignments_completed': 12,
        'assignments_total': 20,
        'next_deadlines': [
            {'title': 'Matrix Operations Quiz', 'due': 'in 2 days'},
            {'title': 'Advanced Theory Assignment', 'due': 'in 5 days'},
            {'title': 'Project Proposal Draft', 'due': 'in 1 week'},
        ],
        'weekly_study_hours': [2.5, 1.5, 3.0, 2.0, 1.0, 4.0, 2.5],  # Mon-Sun
        'course_progress': [
            {'name': 'Engineering 101', 'progress': 68},
            {'name': 'Data Science Basics', 'progress': 62},
            {'name': 'Physics Fundamentals', 'progress': 75},
        ],
        'recommendations': [
            {
                'icon': '🎬',
                'title': 'Video Tutorial',
                'content': 'Matrix Operations Explained',
                'reason': 'Matches your visual learning style'
            },
            {
                'icon': '📝',
                'title': 'Practice Problems',
                'content': 'Interactive Matrix Exercises',
                'reason': 'Reinforces current module'
            },
            {
                'icon': '📊',
                'title': 'Visual Guide',
                'content': 'Differential Equations Diagram',
                'reason': 'Prepares for upcoming topic'
            },
        ],
        # Module-level progress
        'roadmap_data': [
            {
                'module': '1. Introduction',
                'completion': 100,
                'topics': [
                    {'name': 'Course Overview', 'completion': 100},
                    {'name': 'Development Tools', 'completion': 100},
                    {'name': 'Environment Setup', 'completion': 100},
                ]
            },
            {
                'module': '2. Basic Concepts',
                'completion': 80,
                'topics': [
                    {'name': 'Fundamentals', 'completion': 100},
                    {'name': 'Core Principles', 'completion': 100},
                    {'name': 'Practice Exercises', 'completion': 80},
                    {'name': 'Module Assessment', 'completion': 50},
                ]
            },
            {
                'module': '3. Advanced Theory',
                'completion': 45,
                'topics': [
                    {'name': 'Complex Variables', 'completion': 92},
                    {'name': 'Matrix Operations', 'completion': 45},
                    {'name': 'Differential Equations', 'completion': 0},
                    {'name': 'Numerical Methods', 'completion': 0},
                ]
            },
            {
                'module': '4. Applications',
                'completion': 10,
                'topics': [
                    {'name': 'Real-world Case Studies', 'completion': 10},
                    {'name': 'Industry Tools', 'completion': 10},
                    {'name': 'Project Planning', 'completion': 0},
                ]
            },
            {
                'module': '5. Final Project',
                'completion': 0,
                'topics': [
                    {'name': 'Project Proposal', 'completion': 0},
                    {'name': 'Development Phase', 'completion': 0},
                    {'name': 'Final Presentation', 'completion': 0},
                ]
            },
        ]
    },
    'student2': {
        'id': 1002,
        'username': 'student2',
        'name': 'Sam Martinez',
        'email': 'student2@example.com',
        'learning_style': 'Reading/Text',
        'preferred_pace': 'Fast',
        'content_format': 'Articles + Quizzes',
        'overall_progress': 92,
        'current_module': 'Module 5: Final Project',
        'pace_status': 'Ahead',
        'pace_delta': '12 days ahead',
        'last_active': '3 hours ago',
        'risk_level': 'Low',
        'action_needed': 'None',
        'engagement_pattern': 'High Achiever',
        # Dashboard data - high achiever
        'assignments_completed': 19,
        'assignments_total': 20,
        'next_deadlines': [
            {'title': 'Final Project Presentation', 'due': 'in 10 days'},
            {'title': 'Peer Review Submissions', 'due': 'in 12 days'},
            {'title': 'Course Evaluation', 'due': 'in 2 weeks'},
        ],
        'weekly_study_hours': [4.5, 5.0, 4.0, 5.5, 3.5, 6.0, 4.5],  # High study time
        'course_progress': [
            {'name': 'Engineering 101', 'progress': 92},
            {'name': 'Data Science Basics', 'progress': 95},
            {'name': 'Physics Fundamentals', 'progress': 88},
        ],
        'recommendations': [
            {
                'icon': '📚',
                'title': 'Advanced Reading',
                'content': 'Research Paper: ML in Engineering',
                'reason': 'Challenge yourself with advanced material'
            },
            {
                'icon': '🎯',
                'title': 'Quiz Challenge',
                'content': 'Advanced Topics Assessment',
                'reason': 'Test your comprehensive knowledge'
            },
            {
                'icon': '🌟',
                'title': 'Enrichment',
                'content': 'Article: Industry Best Practices',
                'reason': 'Aligns with your reading preference'
            },
        ],
        # Module-level progress - high performer
        'roadmap_data': [
            {
                'module': '1. Introduction',
                'completion': 100,
                'topics': [
                    {'name': 'Course Overview', 'completion': 100},
                    {'name': 'Development Tools', 'completion': 100},
                    {'name': 'Environment Setup', 'completion': 100},
                ]
            },
            {
                'module': '2. Basic Concepts',
                'completion': 100,
                'topics': [
                    {'name': 'Fundamentals', 'completion': 100},
                    {'name': 'Core Principles', 'completion': 100},
                    {'name': 'Practice Exercises', 'completion': 100},
                    {'name': 'Module Assessment', 'completion': 100},
                ]
            },
            {
                'module': '3. Advanced Theory',
                'completion': 100,
                'topics': [
                    {'name': 'Complex Variables', 'completion': 100},
                    {'name': 'Matrix Operations', 'completion': 100},
                    {'name': 'Differential Equations', 'completion': 100},
                    {'name': 'Numerical Methods', 'completion': 100},
                ]
            },
            {
                'module': '4. Applications',
                'completion': 88,
                'topics': [
                    {'name': 'Real-world Case Studies', 'completion': 100},
                    {'name': 'Industry Tools', 'completion': 100},
                    {'name': 'Project Planning', 'completion': 65},
                ]
            },
            {
                'module': '5. Final Project',
                'completion': 60,
                'topics': [
                    {'name': 'Project Proposal', 'completion': 100},
                    {'name': 'Development Phase', 'completion': 75},
                    {'name': 'Final Presentation', 'completion': 5},
                ]
            },
        ]
    },
    'student3': {
        'id': 1003,
        'username': 'student3',
        'name': 'Jordan Lee',
        'email': 'student3@example.com',
        'learning_style': 'Auditory/Visual',
        'preferred_pace': 'Slow',
        'content_format': 'Videos + Discussions',
        'overall_progress': 35,
        'current_module': 'Module 2: Basic Concepts',
        'pace_status': 'Behind',
        'pace_delta': '-5 days behind',
        'last_active': '6 days ago',
        'risk_level': 'High',
        'action_needed': 'Intervention',
        'engagement_pattern': 'Struggling',
        # Dashboard data - struggling student
        'assignments_completed': 6,
        'assignments_total': 20,
        'next_deadlines': [
            {'title': 'Practice Exercises (OVERDUE)', 'due': '2 days ago'},
            {'title': 'Module 2 Assessment', 'due': 'tomorrow'},
            {'title': 'Fundamentals Quiz Retake', 'due': 'in 3 days'},
        ],
        'weekly_study_hours': [0.5, 1.0, 0.0, 1.5, 0.5, 2.0, 1.0],  # Low, inconsistent
        'course_progress': [
            {'name': 'Engineering 101', 'progress': 35},
            {'name': 'Data Science Basics', 'progress': 28},
            {'name': 'Physics Fundamentals', 'progress': 42},
        ],
        'recommendations': [
            {
                'icon': '🎥',
                'title': 'Video Series',
                'content': 'Fundamentals Review Sessions',
                'reason': 'Catch up on missed concepts'
            },
            {
                'icon': '👥',
                'title': 'Discussion Group',
                'content': 'Join Study Group Session',
                'reason': 'Collaborative learning support'
            },
            {
                'icon': '📞',
                'title': 'Office Hours',
                'content': 'One-on-One Tutoring Available',
                'reason': 'Get personalized help'
            },
        ],
        # Module-level progress - struggling student
        'roadmap_data': [
            {
                'module': '1. Introduction',
                'completion': 100,
                'topics': [
                    {'name': 'Course Overview', 'completion': 100},
                    {'name': 'Development Tools', 'completion': 100},
                    {'name': 'Environment Setup', 'completion': 100},
                ]
            },
            {
                'module': '2. Basic Concepts',
                'completion': 42,
                'topics': [
                    {'name': 'Fundamentals', 'completion': 85},
                    {'name': 'Core Principles', 'completion': 60},
                    {'name': 'Practice Exercises', 'completion': 15},
                    {'name': 'Module Assessment', 'completion': 10},
                ]
            },
            {
                'module': '3. Advanced Theory',
                'completion': 0,
                'topics': [
                    {'name': 'Complex Variables', 'completion': 0},
                    {'name': 'Matrix Operations', 'completion': 0},
                    {'name': 'Differential Equations', 'completion': 0},
                    {'name': 'Numerical Methods', 'completion': 0},
                ]
            },
            {
                'module': '4. Applications',
                'completion': 0,
                'topics': [
                    {'name': 'Real-world Case Studies', 'completion': 0},
                    {'name': 'Industry Tools', 'completion': 0},
                    {'name': 'Project Planning', 'completion': 0},
                ]
            },
            {
                'module': '5. Final Project',
                'completion': 0,
                'topics': [
                    {'name': 'Project Proposal', 'completion': 0},
                    {'name': 'Development Phase', 'completion': 0},
                    {'name': 'Final Presentation', 'completion': 0},
                ]
            },
        ]
    }
}

def get_student_profile(username):
    """Get student profile data by username"""
    return REAL_STUDENTS.get(username, None)

def get_all_real_students():
    """Get all real student profiles"""
    return REAL_STUDENTS
