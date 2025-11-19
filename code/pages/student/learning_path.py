# learning_path.py - Auto-extracted from app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.auth import get_user_preferences
from modules.auth import update_user_preferences


def display_learning_path():
    st.title("My Learning Path")

    # Get student-specific data
    from modules.student_data import get_student_profile
    username = st.session_state.get('username', 'student1')
    student_profile = get_student_profile(username)

    # Use default data if no profile found
    if not student_profile:
        student_profile = {
            'overall_progress': 68,
            'current_module': 'Module 3: Advanced Theory',
            'pace_status': 'On Track',
            'pace_delta': '2 days ahead',
            'roadmap_data': []
        }

    # Overview metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Progress", f"{student_profile['overall_progress']}%")
    with col2:
        st.metric("Current Module", student_profile['current_module'])
    with col3:
        st.metric("Pace", student_profile['pace_status'], delta=student_profile['pace_delta'])

    # Roadmap-style Learning Path Visualization
    st.markdown("---")
    st.subheader("🗺️ Your Learning Roadmap")

    # Get roadmap data from student profile
    roadmap_data = student_profile.get('roadmap_data', [])

    # Helper function to get status styling
    def get_status_style(completion):
        if completion == 100:
            return {
                'bg_color': '#d4edda',
                'border_color': '#28a745',
                'text_color': '#155724',
                'icon': '✅',
                'status': 'Completed'
            }
        elif completion >= 50:
            return {
                'bg_color': '#fff3cd',
                'border_color': '#ffc107',
                'text_color': '#856404',
                'icon': '🔄',
                'status': 'In Progress'
            }
        elif completion > 0:
            return {
                'bg_color': '#d1ecf1',
                'border_color': '#17a2b8',
                'text_color': '#0c5460',
                'icon': '🚀',
                'status': 'Started'
            }
        else:
            return {
                'bg_color': '#f8f9fa',
                'border_color': '#6c757d',
                'text_color': '#6c757d',
                'icon': '🔒',
                'status': 'Locked'
            }

    # Render roadmap
    for idx, module_data in enumerate(roadmap_data):
        module_name = module_data['module']
        module_completion = module_data['completion']
        topics = module_data['topics']

        style = get_status_style(module_completion)

        # Module header box
        st.markdown(f"""
        <div style="
            background-color: {style['bg_color']};
            border-left: 5px solid {style['border_color']};
            border-radius: 8px;
            padding: 16px 20px;
            margin: 20px 0 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; color: {style['text_color']};">
                    {style['icon']} {module_name}
                </h3>
                <span style="
                    background-color: white;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-weight: bold;
                    color: {style['text_color']};
                    font-size: 14px;
                ">
                    {module_completion}%
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Topics grid
        cols = st.columns(len(topics))
        for col, topic in zip(cols, topics):
            topic_style = get_status_style(topic['completion'])

            with col:
                st.markdown(f"""
                <div style="
                    background-color: white;
                    border: 2px solid {topic_style['border_color']};
                    border-radius: 8px;
                    padding: 12px;
                    text-align: center;
                    min-height: 100px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                ">
                    <div style="font-size: 24px; margin-bottom: 8px;">
                        {topic_style['icon']}
                    </div>
                    <div style="
                        font-weight: 600;
                        color: #333;
                        font-size: 13px;
                        margin-bottom: 8px;
                        line-height: 1.3;
                    ">
                        {topic['name']}
                    </div>
                    <div style="
                        background-color: {topic_style['bg_color']};
                        padding: 3px 8px;
                        border-radius: 10px;
                        font-size: 12px;
                        font-weight: bold;
                        color: {topic_style['text_color']};
                    ">
                        {topic['completion']}%
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Connecting arrow (except for last module)
        if idx < len(roadmap_data) - 1:
            st.markdown("""
            <div style="text-align: center; margin: 15px 0; font-size: 30px; color: #6c757d;">
                ↓
            </div>
            """, unsafe_allow_html=True)

    # Legend
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**✅ Completed** - 100%")
    with col2:
        st.markdown("**🔄 In Progress** - 50-99%")
    with col3:
        st.markdown("**🚀 Started** - 1-49%")
    with col4:
        st.markdown("**🔒 Locked** - 0%")

    st.info("💡 **Tip:** Progress through modules from top to bottom. Complete all topics in a module before moving to the next!")

    # Learning path visualization
    st.markdown("---")
    st.subheader("Your Learning Journey - Linear Progress")

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

    st.plotly_chart(fig, width="stretch")
    
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
        if user_prefs and user_prefs['learning_preference']:
            st.markdown(f"**Learning Preference:** {user_prefs['learning_preference']}")
            st.markdown(f"**Preferred Pace:** {user_prefs['preferred_pace']}")
            st.markdown(f"**Content Format:** {user_prefs['content_format']}")
        else:
            st.info("No learning preferences set. Take the assessment to personalize your experience!")

    with col2:
        st.markdown("### Update Preferences")
        if st.button("Update Learning Preferences", key="update_prefs_btn"):
            st.session_state.show_preferences_form = True
        if st.button("Take Learning Preference Assessment", key="take_assessment_btn"):
            st.session_state.show_assessment = True

    # Radar chart visualization of learning style
    if user_prefs and user_prefs['learning_preference']:
        st.markdown("---")
        st.subheader("Your Learning Profile")

        # Map learning preference to scores for radar chart
        learning_preference_scores = {
            "Visual/Interactive": {"Visual": 90, "Reading": 40, "Auditory": 50, "Kinesthetic": 70},
            "Reading/Text": {"Visual": 40, "Reading": 95, "Auditory": 30, "Kinesthetic": 35},
            "Auditory/Visual": {"Visual": 75, "Reading": 45, "Auditory": 90, "Kinesthetic": 40},
            "Kinesthetic/Hands-on": {"Visual": 55, "Reading": 35, "Auditory": 40, "Kinesthetic": 95},
            "Mixed": {"Visual": 70, "Reading": 70, "Auditory": 70, "Kinesthetic": 70}
        }

        # Get scores for current learning preference
        current_style = user_prefs['learning_preference']
        scores = learning_preference_scores.get(current_style, {"Visual": 50, "Reading": 50, "Auditory": 50, "Kinesthetic": 50})

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
                text=f"Learning Preference Profile: {current_style}",
                x=0.5,
                xanchor='center'
            ),
            height=450,
            margin=dict(l=80, r=80, t=80, b=40)
        )

        st.plotly_chart(fig, width="stretch")

    # Show preferences update form
    if st.session_state.get('show_preferences_form', False):
        st.markdown("---")
        st.subheader("Update Your Learning Preferences")

        with st.form("learning_preferences_form"):
            col1, col2, col3 = st.columns(3)

            with col1:
                learning_preference = st.selectbox(
                    "Learning Preference",
                    ["Visual/Interactive", "Reading/Text", "Auditory/Visual", "Kinesthetic/Hands-on", "Mixed"],
                    index=0 if not user_prefs or not user_prefs['learning_preference'] else
                          ["Visual/Interactive", "Reading/Text", "Auditory/Visual", "Kinesthetic/Hands-on", "Mixed"].index(user_prefs['learning_preference'])
                          if user_prefs['learning_preference'] in ["Visual/Interactive", "Reading/Text", "Auditory/Visual", "Kinesthetic/Hands-on", "Mixed"] else 0,
                    key="pref_learning_preference"
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
                    learning_preference=learning_preference,
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

    # Show learning preference assessment
    if st.session_state.get('show_assessment', False):
        st.markdown("---")
        st.subheader("Learning Preference Assessment")
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
                # Determine learning preference based on answers
                visual_score = (1 if "videos" in q1.lower() else 0) + (1 if "videos" in q2.lower() else 0) + (1 if "Visual" in q4 else 0)
                reading_score = (1 if "reading" in q1.lower() else 0) + (1 if "Reading" in q2.lower() else 0) + (1 if "Written" in q4 else 0)
                auditory_score = (1 if "listening" in q1.lower() else 0) + (1 if "discussions" in q2.lower() else 0) + (1 if "Discussion" in q4 else 0)
                kinesthetic_score = (1 if "hands-on" in q1.lower() else 0) + (1 if "practice" in q2.lower() else 0) + (1 if "Practical" in q4 else 0)

                # Determine primary learning preference
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
                    learning_preference=primary_style,
                    preferred_pace=pace,
                    content_format=content
                )

                if success:
                    st.success(f"✅ Assessment complete! Your learning preference is: **{primary_style}**")
                    st.info(f"Based on your responses, we recommend: {content} at a {pace} pace.")
                    st.session_state.show_assessment = False
                    st.balloons()
                    st.rerun()
                else:
                    st.error(message)

            if assess_cancel:
                st.session_state.show_assessment = False
                st.rerun()




