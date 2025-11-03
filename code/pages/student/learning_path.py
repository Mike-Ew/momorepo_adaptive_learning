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

    # Create network graph tree structure with nodes and edges
    import numpy as np

    # Define tree structure with hierarchical positions
    tree_nodes = [
        # (id, label, completion, parent_id, level)
        (0, 'Engineering<br>Course', 68, None, 0),
        # Level 1 - Main modules
        (1, '1. Introduction', 100, 0, 1),
        (2, '2. Basic<br>Concepts', 80, 0, 1),
        (3, '3. Advanced<br>Theory', 45, 0, 1),
        (4, '4. Applications', 10, 0, 1),
        (5, '5. Final<br>Project', 0, 0, 1),
        # Level 2 - Topics
        (6, '1.1 Overview', 100, 1, 2),
        (7, '1.2 Tools', 100, 1, 2),
        (8, '1.3 Setup', 100, 1, 2),
        (9, '2.1 Fundamentals', 100, 2, 2),
        (10, '2.2 Core Principles', 100, 2, 2),
        (11, '2.3 Practice', 80, 2, 2),
        (12, '2.4 Assessment', 50, 2, 2),
        (13, '3.1 Complex Var', 92, 3, 2),
        (14, '3.2 Matrix Ops', 45, 3, 2),
        (15, '3.3 Diff Eq', 0, 3, 2),
        (16, '3.4 Numerical', 0, 3, 2),
        (17, '4.1 Real Cases', 10, 4, 2),
        (18, '4.2 Industry Tools', 10, 4, 2),
        (19, '4.3 Planning', 0, 4, 2),
        (20, '5.1 Proposal', 0, 5, 2),
        (21, '5.2 Development', 0, 5, 2),
        (22, '5.3 Presentation', 0, 5, 2),
    ]

    # Calculate positions for tree layout
    def get_node_positions(nodes):
        positions = {}
        level_counts = {}
        level_indices = {}

        # Count nodes per level
        for node_id, label, comp, parent_id, level in nodes:
            level_counts[level] = level_counts.get(level, 0) + 1

        # Initialize level indices
        for level in level_counts:
            level_indices[level] = 0

        # Assign positions
        for node_id, label, comp, parent_id, level in nodes:
            y = -level * 1.5  # Vertical position (top to bottom)

            # Horizontal position - spread evenly
            total_in_level = level_counts[level]
            index = level_indices[level]
            level_indices[level] += 1

            # Center the nodes
            x = (index - (total_in_level - 1) / 2) * 2

            positions[node_id] = (x, y)

        return positions

    positions = get_node_positions(tree_nodes)

    # Create edges (connecting lines)
    edge_x = []
    edge_y = []

    for node_id, label, comp, parent_id, level in tree_nodes:
        if parent_id is not None:
            x0, y0 = positions[parent_id]
            x1, y1 = positions[node_id]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

    # Create edge trace
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    # Create node traces (separate by completion status for coloring)
    node_data = {'completed': [], 'in_progress': [], 'started': [], 'locked': []}

    for node_id, label, comp, parent_id, level in tree_nodes:
        x, y = positions[node_id]

        if comp == 100:
            category = 'completed'
            status = "✅ Completed"
        elif comp >= 50:
            category = 'in_progress'
            status = "🔄 In Progress"
        elif comp > 0:
            category = 'started'
            status = "🚀 Started"
        else:
            category = 'locked'
            status = "🔒 Locked"

        node_data[category].append({
            'x': x, 'y': y, 'label': label.replace('<br>', ' '),
            'hover': f"<b>{label.replace('<br>', ' ')}</b><br>{status}<br>Progress: {comp}%"
        })

    # Color mapping
    color_map = {
        'completed': '#28a745',    # Green
        'in_progress': '#ffc107',  # Orange
        'started': '#17a2b8',      # Blue
        'locked': '#6c757d'        # Gray
    }

    # Create node traces
    node_traces = []
    for category, nodes in node_data.items():
        if nodes:
            node_traces.append(go.Scatter(
                x=[n['x'] for n in nodes],
                y=[n['y'] for n in nodes],
                mode='markers+text',
                marker=dict(
                    size=25,
                    color=color_map[category],
                    line=dict(width=2, color='white')
                ),
                text=[n['label'] for n in nodes],
                textposition="middle center",
                textfont=dict(size=9, color='white', family='Arial Black'),
                hovertext=[n['hover'] for n in nodes],
                hoverinfo='text',
                name=category.replace('_', ' ').title()
            ))

    # Create figure
    fig_tree = go.Figure(data=[edge_trace] + node_traces)

    fig_tree.update_layout(
        title={
            'text': "Skills Tree - Your Learning Path",
            'x': 0.5,
            'xanchor': 'center'
        },
        showlegend=False,
        hovermode='closest',
        height=650,
        margin=dict(t=50, l=20, r=20, b=20),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        paper_bgcolor='white'
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

    st.info("💡 **Tip:** Hover over nodes to see detailed progress information. Lines connect parent topics to their subtopics.")

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


