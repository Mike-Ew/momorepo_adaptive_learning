# analytics.py - Auto-extracted from app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


def display_analytics():
    st.title("Learning Analytics")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.role == "admin":
            course_options = ["All Courses", "Engineering 101", "Data Science Basics", "Advanced AI"]
        else:  # teacher
            course_options = ["Engineering 101", "Data Science Basics", "Advanced AI"]
        
        selected_course = st.selectbox("Course", course_options)
    
    with col2:
        time_period = st.selectbox("Time Period", ["Last Week", "Last Month", "This Semester", "All Time"])
    
    with col3:
        metric_focus = st.selectbox("Metric Focus", ["Engagement", "Performance", "Risk", "Content Effectiveness"])
    
    # Overview metrics
    st.subheader("Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Engagement Score", "76%", delta="3%")
    with col2:
        st.metric("Average Performance", "82%", delta="-1%")
    with col3:
        st.metric("At-Risk Students", "15%", delta="-2%")
    with col4:
        st.metric("Content Effectiveness", "Medium")
    
    # Main analytics based on selected focus
    if metric_focus == "Engagement":
        st.subheader("Engagement Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Engagement Over Time")
            # Mock engagement data
            dates = pd.date_range(start='2025-01-01', periods=10, freq='W')
            engagement = [68, 72, 75, 73, 76, 79, 78, 82, 80, 76]
            
            engagement_data = pd.DataFrame({
                'Date': dates,
                'Engagement': engagement
            })
            
            st.line_chart(engagement_data.set_index('Date'))
        
        with col2:
            st.markdown("### Engagement by Activity Type")
            
            activity_types = ['Video Lectures', 'Readings', 'Discussions', 'Practice Problems', 'Assessments']
            activity_scores = [85, 65, 72, 80, 78]
            
            activity_data = pd.DataFrame({
                'Activity': activity_types,
                'Engagement': activity_scores
            })
            
            fig = px.bar(
                activity_data, 
                y='Activity', 
                x='Engagement', 
                orientation='h',
                color='Engagement',
                color_continuous_scale='blues'
            )
            
            st.plotly_chart(fig)
        
        # Engagement patterns
        st.subheader("Engagement Patterns")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Time of Day Activity")
            
            hours = list(range(24))
            activity = [5, 3, 1, 0, 0, 2, 8, 15, 25, 28, 20, 18, 22, 25, 28, 30, 25, 18, 15, 12, 10, 8, 7, 6]
            
            time_data = pd.DataFrame({
                'Hour': [f"{h:02d}:00" for h in hours],
                'Activity': activity
            })
            
            st.bar_chart(time_data.set_index('Hour'))
        
        with col2:
            st.markdown("### Day of Week Activity")
            
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_activity = [85, 82, 78, 75, 65, 45, 55]
            
            day_data = pd.DataFrame({
                'Day': days,
                'Activity': day_activity
            })
            
            st.bar_chart(day_data.set_index('Day'))
    
    elif metric_focus == "Performance":
        st.subheader("Performance Analytics")
        
        # Grade distribution
        st.markdown("### Grade Distribution")
        
        grade_ranges = ['90-100%', '80-89%', '70-79%', '60-69%', 'Below 60%']
        student_counts = [15, 25, 35, 18, 7]
        
        grade_data = pd.DataFrame({
            'Grade Range': grade_ranges,
            'Student Count': student_counts
        })
        
        fig = px.bar(
            grade_data,
            x='Grade Range',
            y='Student Count',
            color='Student Count',
            color_continuous_scale='blues',
            text='Student Count'
        )
        fig.update_traces(textposition='outside')
        
        st.plotly_chart(fig)
        
        # Performance by assessment type
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Performance by Assessment Type")
            
            assessment_types = ['Quizzes', 'Homework', 'Projects', 'Exams']
            performance = [78, 82, 75, 70]
            
            assessment_data = pd.DataFrame({
                'Type': assessment_types,
                'Average Score': performance
            })
            
            st.bar_chart(assessment_data.set_index('Type'))
        
        with col2:
            st.markdown("### Performance by Topic")
            
            topics = ['Topic 1', 'Topic 2', 'Topic 3', 'Topic 4', 'Topic 5']
            topic_scores = [85, 78, 65, 72, 80]
            
            topic_data = pd.DataFrame({
                'Topic': topics,
                'Average Score': topic_scores
            })
            
            st.bar_chart(topic_data.set_index('Topic'))
        
        # Detailed assessment performance
        st.markdown("### Assessment Performance Details")
        
        assessments = pd.DataFrame({
            'Assessment': ['Quiz 1', 'Homework 1', 'Quiz 2', 'Project 1', 'Midterm', 'Quiz 3'],
            'Average': [78, 82, 75, 85, 72, 80],
            'Median': [80, 85, 78, 88, 75, 82],
            'Highest': [95, 98, 92, 100, 90, 96],
            'Lowest': [45, 55, 40, 60, 38, 52],
            'Std Dev': [12, 10, 15, 11, 14, 12]
        })
        
        st.dataframe(assessments)
    
    elif metric_focus == "Risk":
        st.subheader("Risk Analytics")
        
        # Risk distribution
        st.markdown("### Student Risk Distribution")
        
        risk_levels = ['Low Risk', 'Moderate Risk', 'High Risk', 'Severe Risk']
        risk_counts = [65, 20, 10, 5]
        
        risk_data = pd.DataFrame({
            'Risk Level': risk_levels,
            'Student Count': risk_counts
        })
        
        fig = px.pie(
            risk_data,
            values='Student Count',
            names='Risk Level',
            color='Risk Level',
            color_discrete_map={
                'Low Risk': 'green',
                'Moderate Risk': 'yellow',
                'High Risk': 'orange',
                'Severe Risk': 'red'
            }
        )
        
        st.plotly_chart(fig)
        
        # Risk factors
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Primary Risk Factors")
            
            risk_factors = [
                'Low Engagement',
                'Missing Assignments',
                'Poor Quiz Performance',
                'Infrequent Logins',
                'Limited Resource Access'
            ]
            
            factor_impact = [35, 25, 20, 15, 5]
            
            factor_data = pd.DataFrame({
                'Factor': risk_factors,
                'Impact': factor_impact
            })
            
            fig = px.bar(
                factor_data,
                y='Factor',
                x='Impact',
                orientation='h',
                color='Impact',
                color_continuous_scale='reds'
            )
            
            st.plotly_chart(fig)
        
        with col2:
            st.markdown("### Risk Trend")
            
            weeks = [f"Week {i}" for i in range(1, 11)]
            high_risk = [8, 7, 9, 12, 15, 14, 12, 10, 12, 15]
            
            risk_trend = pd.DataFrame({
                'Week': weeks,
                'High Risk Students': high_risk
            })
            
            st.line_chart(risk_trend.set_index('Week'))
        
        # Intervention effectiveness
        st.markdown("### Intervention Effectiveness")
        
        interventions = pd.DataFrame({
            'Intervention Type': ['Automated Reminders', 'Personalized Resources', 'Instructor Outreach', 'Deadline Extensions', 'Study Groups'],
            'Implementation Rate': [95, 75, 60, 45, 30],
            'Success Rate': [65, 80, 85, 70, 75],
            'Average Risk Reduction': ['15%', '25%', '35%', '20%', '22%']
        })
        
        st.dataframe(interventions)
    
    elif metric_focus == "Content Effectiveness":
        st.subheader("Content Effectiveness Analytics")
        
        # Content engagement
        st.markdown("### Content Engagement Rates")
        
        content_types = ['Video Lectures', 'Readings', 'Interactive Simulations', 'Practice Problems', 'Discussion Forums']
        completion_rates = [75, 62, 88, 70, 45]
        avg_time = [25, 35, 20, 40, 15]
        
        content_data = pd.DataFrame({
            'Content Type': content_types,
            'Completion Rate': completion_rates,
            'Avg. Time (min)': avg_time
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                content_data,
                x='Content Type',
                y='Completion Rate',
                color='Completion Rate',
                color_continuous_scale='blues',
                text='Completion Rate'
            )
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            
            st.plotly_chart(fig)
        
        with col2:
            fig = px.bar(
                content_data,
                x='Content Type',
                y='Avg. Time (min)',
                color='Avg. Time (min)',
                color_continuous_scale='viridis',
                text='Avg. Time (min)'
            )
            fig.update_traces(textposition='outside')
            
            st.plotly_chart(fig)
        
        # Content effectiveness by module
        st.markdown("### Content Effectiveness by Module")
        
        modules = ['Module 1', 'Module 2', 'Module 3', 'Module 4', 'Module 5']
        effectiveness = [85, 75, 65, 80, 70]
        complexity = [25, 45, 75, 60, 80]
        
        module_data = pd.DataFrame({
            'Module': modules,
            'Effectiveness': effectiveness,
            'Complexity': complexity
        })
        
        fig = px.scatter(
            module_data,
            x='Complexity',
            y='Effectiveness',
            text='Module',
            size=[40] * len(modules),
            color='Effectiveness',
            color_continuous_scale='blues'
        )
        
        st.plotly_chart(fig)
        
        # Content improvement recommendations
        st.markdown("### Content Improvement Recommendations")
        
        recommendations = pd.DataFrame({
            'Content Item': ['Video 2.3', 'Reading 3.1', 'Quiz 2', 'Simulation 1.2', 'Homework 3'],
            'Current Effectiveness': ['Low', 'Medium', 'Low', 'Medium', 'Low'],
            'Issue': ['Too long', 'Too complex', 'Unclear questions', 'Technical issues', 'Misaligned difficulty'],
            'Recommendation': ['Split into smaller segments', 'Add supporting materials', 'Revise questions', 'Fix loading issues', 'Adjust difficulty level']
        })
        
        st.dataframe(recommendations)


