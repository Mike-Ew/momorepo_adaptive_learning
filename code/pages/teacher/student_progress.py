# student_progress.py - Auto-extracted from app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def display_student_progress():
    st.title("Student Progress Monitoring")
    
    # Class selector
    classes = ["Engineering 101", "Data Science Basics", "Advanced AI"]
    selected_class = st.selectbox("Select Class", classes)
    
    # Overview metrics
    st.subheader(f"{selected_class} Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Class Average", "76%")
    with col2:
        st.metric("Completion Rate", "68%")
    with col3:
        st.metric("At-Risk Students", "4", delta="-2")
    with col4:
        st.metric("Engagement Score", "Medium")
    
    # Learning Style Distribution for the class
    st.subheader("Class Learning Style Distribution")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Mock class learning style data (in production, aggregate from all students)
        learning_styles_count = {
            "Visual/Interactive": 10,
            "Reading/Text": 6,
            "Auditory/Visual": 5,
            "Kinesthetic/Hands-on": 3,
            "Mixed": 1
        }

        # Create pie chart
        fig_pie = px.pie(
            values=list(learning_styles_count.values()),
            names=list(learning_styles_count.keys()),
            title="Learning Style Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown("### Class Insights")
        st.metric("Most Common Style", "Visual/Interactive", "40%")
        st.metric("Least Common Style", "Mixed", "4%")

        st.markdown("### Teaching Strategy")
        st.info("""
        **Recommendations for this class:**

        • Prioritize visual content (videos, diagrams)

        • Provide text alternatives for readers

        • Include discussion opportunities

        • Offer varied content formats
        """)

    # Average class learning profile radar chart
    st.subheader("Average Class Learning Profile")

    # Calculate average scores across all learning styles in the class
    avg_scores = {"Visual": 0, "Reading": 0, "Auditory": 0, "Kinesthetic": 0}

    learning_style_scores = {
        "Visual/Interactive": {"Visual": 90, "Reading": 40, "Auditory": 50, "Kinesthetic": 70},
        "Reading/Text": {"Visual": 40, "Reading": 95, "Auditory": 30, "Kinesthetic": 35},
        "Auditory/Visual": {"Visual": 75, "Reading": 45, "Auditory": 90, "Kinesthetic": 40},
        "Kinesthetic/Hands-on": {"Visual": 55, "Reading": 35, "Auditory": 40, "Kinesthetic": 95},
        "Mixed": {"Visual": 70, "Reading": 70, "Auditory": 70, "Kinesthetic": 70}
    }

    # Calculate weighted average based on distribution
    total_students = sum(learning_styles_count.values())
    for style, count in learning_styles_count.items():
        weight = count / total_students
        style_scores = learning_style_scores[style]
        for dimension in avg_scores:
            avg_scores[dimension] += style_scores[dimension] * weight

    categories = list(avg_scores.keys())
    values = list(avg_scores.values())

    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Class Average',
        fillcolor='rgba(46, 204, 113, 0.4)',
        line=dict(color='rgba(46, 204, 113, 1)', width=2)
    ))

    fig_radar.update_layout(
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
            text="Class Average Learning Profile",
            x=0.5,
            xanchor='center'
        ),
        height=400,
        margin=dict(l=60, r=60, t=60, b=40)
    )

    st.plotly_chart(fig_radar, use_container_width=True)

    # Progress distribution
    st.markdown("---")
    st.subheader("Progress Distribution")

    # Mock progress data
    progress_ranges = ['0-25%', '26-50%', '51-75%', '76-100%']
    student_counts = [2, 5, 10, 8]

    fig = px.bar(
        x=progress_ranges,
        y=student_counts,
        labels={'x': 'Progress Range', 'y': 'Number of Students'},
        color=student_counts,
        color_continuous_scale='blues'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Student list with risk levels
    st.subheader("Student List")
    
    # Add filters
    col1, col2, col3 = st.columns(3)
    with col1:
        risk_filter = st.multiselect("Risk Level", ["High", "Medium", "Low"], default=[])
    with col2:
        progress_filter = st.slider("Progress Range", 0, 100, (0, 100))
    with col3:
        sort_by = st.selectbox("Sort By", ["Risk (High to Low)", "Progress (Low to High)", "Name"])
    
    # Mock student data
    students = pd.DataFrame({
        'Student ID': range(1001, 1026),
        'Name': [f"Student {i}" for i in range(1, 26)],
        'Progress': np.random.uniform(20, 95, 25),
        'Last Active': [f"{i} days ago" for i in np.random.randint(1, 10, 25)],
        'Risk Level': np.random.choice(['Low', 'Medium', 'High'], 25, p=[0.7, 0.2, 0.1]),
        'Action Needed': np.random.choice(['None', 'Check-in', 'Intervention'], 25, p=[0.6, 0.3, 0.1])
    })
    
    # Apply filters
    if risk_filter:
        students = students[students['Risk Level'].isin(risk_filter)]
    
    students = students[(students['Progress'] >= progress_filter[0]) & 
                       (students['Progress'] <= progress_filter[1])]
    
    # Apply sorting
    if sort_by == "Risk (High to Low)":
        risk_order = {'High': 0, 'Medium': 1, 'Low': 2}
        students['Risk Order'] = students['Risk Level'].map(risk_order)
        students = students.sort_values('Risk Order')
        students = students.drop('Risk Order', axis=1)
    elif sort_by == "Progress (Low to High)":
        students = students.sort_values('Progress')
    else:  # Name
        students = students.sort_values('Name')
    
    # Format progress as percentage
    students['Progress'] = students['Progress'].apply(lambda x: f"{x:.1f}%")
    
    # Display student table
    st.dataframe(students)
    
    # Individual student analysis
    st.subheader("Individual Student Analysis")

    selected_student = st.selectbox("Select Student", students['Name'], key="individual_student_select")

    col1, col2 = st.columns(2)
    with col1:
        # Mock individual student data
        st.markdown(f"### {selected_student}")
        st.markdown("**Progress:** 67.5%")
        st.markdown("**Risk Level:** Medium")
        st.markdown("**Last Active:** 2 days ago")
        st.markdown("**Learning Style:** Visual/Interactive")
        st.markdown("**Preferred Pace:** Moderate")
        st.markdown("**Content Format:** Video + Practice Problems")
        st.markdown("**Engagement Pattern:** Sporadic")

        # Actions
        st.button("Send Message", key="teacher_send_msg")
        st.button("Adjust Schedule", key="teacher_adjust_schedule")
        st.button("Provide Resources", key="teacher_provide_resources")

    with col2:
        # Activity timeline
        st.markdown("### Recent Activity")
        activities = [
            "Completed Quiz 3 (Score: 75%)",
            "Viewed Lecture 5",
            "Submitted Assignment 2 (Late)",
            "Started Topic 3.2",
            "Posted in Discussion Forum"
        ]
        activity_dates = [
            "2 days ago",
            "2 days ago",
            "5 days ago",
            "1 week ago",
            "1 week ago"
        ]

        for i in range(len(activities)):
            st.markdown(f"**{activity_dates[i]}:** {activities[i]}")

    # Learning style visualization for individual student
    st.markdown("---")
    st.subheader(f"{selected_student}'s Learning Profile")

    # Mock learning style for demonstration (in production, fetch from user data)
    student_learning_style = "Visual/Interactive"  # This would come from get_user_preferences()

    learning_style_scores = {
        "Visual/Interactive": {"Visual": 90, "Reading": 40, "Auditory": 50, "Kinesthetic": 70},
        "Reading/Text": {"Visual": 40, "Reading": 95, "Auditory": 30, "Kinesthetic": 35},
        "Auditory/Visual": {"Visual": 75, "Reading": 45, "Auditory": 90, "Kinesthetic": 40},
        "Kinesthetic/Hands-on": {"Visual": 55, "Reading": 35, "Auditory": 40, "Kinesthetic": 95},
        "Mixed": {"Visual": 70, "Reading": 70, "Auditory": 70, "Kinesthetic": 70}
    }

    scores = learning_style_scores.get(student_learning_style, {"Visual": 50, "Reading": 50, "Auditory": 50, "Kinesthetic": 50})

    col1, col2 = st.columns([2, 1])

    with col1:
        # Create radar chart
        categories = list(scores.keys())
        values = list(scores.values())

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=student_learning_style,
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
                text=f"Learning Style: {student_learning_style}",
                x=0.5,
                xanchor='center'
            ),
            height=400,
            margin=dict(l=60, r=60, t=60, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Teaching Recommendations")
        st.info("""
        **Based on this student's learning profile:**

        ✓ Emphasize visual materials and diagrams

        ✓ Include hands-on practice exercises

        ✓ Use video tutorials when possible

        ✓ Provide interactive simulations

        ✓ Limit text-heavy readings
        """)

        st.markdown("### Content Preferences")
        st.success("**Best Format:** Video + Practice Problems")
        st.success("**Preferred Pace:** Moderate")


