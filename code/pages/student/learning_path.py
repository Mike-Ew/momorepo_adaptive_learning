# learning_path.py - Auto-extracted from app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.auth import get_user_preferences
from modules.auth import update_user_preferences


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

    # Skills Tree Visualization
    st.markdown("---")
    st.subheader("🌳 Skills Tree - Your Learning Path")

    # Create interactive skills tree using Plotly Sunburst
    skills_data = {
        'labels': [
            # Root
            'Engineering Course',
            # Level 1 - Main modules
            '1. Introduction', '2. Basic Concepts', '3. Advanced Theory', '4. Applications', '5. Final Project',
            # Level 2 - Topics under each module
            '1.1 Overview', '1.2 Tools', '1.3 Setup',
            '2.1 Fundamentals', '2.2 Core Principles', '2.3 Practice', '2.4 Assessment',
            '3.1 Complex Variables', '3.2 Matrix Operations', '3.3 Differential Eq', '3.4 Numerical Methods',
            '4.1 Real-world Cases', '4.2 Industry Tools', '4.3 Project Planning',
            '5.1 Proposal', '5.2 Development', '5.3 Presentation'
        ],
        'parents': [
            # Root parent
            '',
            # Level 1 parents (all belong to root)
            'Engineering Course', 'Engineering Course', 'Engineering Course', 'Engineering Course', 'Engineering Course',
            # Level 2 parents
            '1. Introduction', '1. Introduction', '1. Introduction',
            '2. Basic Concepts', '2. Basic Concepts', '2. Basic Concepts', '2. Basic Concepts',
            '3. Advanced Theory', '3. Advanced Theory', '3. Advanced Theory', '3. Advanced Theory',
            '4. Applications', '4. Applications', '4. Applications',
            '5. Final Project', '5. Final Project', '5. Final Project'
        ],
        'values': [
            # Root
            100,
            # Level 1
            15, 25, 20, 20, 20,
            # Level 2
            5, 5, 5,
            6, 6, 7, 6,
            5, 5, 5, 5,
            7, 7, 6,
            7, 7, 6
        ],
        'completion': [
            # Root
            68,
            # Level 1 - Completion percentages
            100, 80, 45, 10, 0,
            # Level 2 - Topic completion
            100, 100, 100,
            100, 100, 80, 50,
            92, 45, 0, 0,
            10, 10, 0,
            0, 0, 0
        ]
    }

    # Create color coding based on completion
    colors = []
    for completion in skills_data['completion']:
        if completion == 100:
            colors.append('#28a745')  # Green - Completed ✅
        elif completion >= 50:
            colors.append('#ffc107')  # Orange - In Progress 🔄
        elif completion > 0:
            colors.append('#17a2b8')  # Blue - Started 🚀
        else:
            colors.append('#6c757d')  # Gray - Locked 🔒

    # Create hover text with status
    hover_texts = []
    for i, (label, comp) in enumerate(zip(skills_data['labels'], skills_data['completion'])):
        if comp == 100:
            status = "✅ Completed"
        elif comp >= 50:
            status = "🔄 In Progress"
        elif comp > 0:
            status = "🚀 Started"
        else:
            status = "🔒 Locked"
        hover_texts.append(f"<b>{label}</b><br>{status}<br>Progress: {comp}%")

    fig_tree = go.Figure(go.Sunburst(
        labels=skills_data['labels'],
        parents=skills_data['parents'],
        values=skills_data['values'],
        marker=dict(
            colors=colors,
            line=dict(color='white', width=2)
        ),
        text=hover_texts,
        hovertemplate='%{text}<extra></extra>',
        branchvalues="total",
    ))

    fig_tree.update_layout(
        title={
            'text': "Click on sections to explore your learning path",
            'x': 0.5,
            'xanchor': 'center'
        },
        height=600,
        margin=dict(t=50, l=0, r=0, b=0)
    )

    st.plotly_chart(fig_tree, use_container_width=True)

    # Legend
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**✅ Completed** - 100%")
    with col2:
        st.markdown("**🔄 In Progress** - 50-99%")
    with col3:
        st.markdown("**🚀 Started** - 1-49%")
    with col4:
        st.markdown("**🔒 Locked** - 0%")

    st.info("💡 **Tip:** Click on any section in the tree to zoom in and explore sub-topics!")

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


