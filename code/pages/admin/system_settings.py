# system_settings.py - System settings page for admins
import streamlit as st


def display_system_settings():
    """Admin page for system configuration"""
    st.title("System Settings")

    # System settings tabs
    tab1, tab2, tab3, tab4 = st.tabs(["General", "AI Configuration", "Integration", "Backup & Maintenance"])

    with tab1:
        st.subheader("General Settings")

        st.markdown("### Application Configuration")
        col1, col2 = st.columns(2)

        with col1:
            st.text_input("Platform Name", value="Adaptive Learning Platform")
            st.selectbox("Default Language", ["English", "Spanish", "French", "German", "Chinese"])
            st.selectbox("Time Zone", ["UTC", "US/Eastern", "US/Central", "US/Pacific", "Europe/London"])
            st.number_input("Session Timeout (minutes)", value=30)

        with col2:
            st.checkbox("Enable Multi-factor Authentication", value=True)
            st.checkbox("Allow Self-registration", value=True)
            st.checkbox("Enable Notifications", value=True)
            st.checkbox("Enable Analytics", value=True)

        st.markdown("### Email Configuration")
        st.text_input("SMTP Server")
        st.text_input("SMTP Port")
        st.text_input("Email Username")
        st.text_input("Email Password", type="password")
        st.text_input("Sender Email")
        st.checkbox("Enable SSL/TLS", value=True)

        st.button("Save General Settings")

    with tab2:
        st.subheader("AI Configuration")

        st.markdown("### Recommendation Engine")
        col1, col2 = st.columns(2)

        with col1:
            st.selectbox("Algorithm Type", ["Multi-armed Bandit", "Collaborative Filtering", "Content-based Filtering", "Hybrid"])
            st.slider("Exploration Rate", 0.0, 1.0, 0.2)
            st.number_input("Minimum Data Points Required", value=10)
            st.checkbox("Allow Real-time Updates", value=True)

        with col2:
            st.multiselect("Features to Consider",
                          ["Quiz Performance", "Assignment Completion", "Time Spent", "Learning Style", "Previous Course Performance"],
                          default=["Quiz Performance", "Assignment Completion", "Time Spent"])
            st.slider("Performance Weight", 0.0, 1.0, 0.7)
            st.slider("Engagement Weight", 0.0, 1.0, 0.3)

        st.markdown("### Risk Detection Model")
        col1, col2 = st.columns(2)

        with col1:
            st.selectbox("Model Type", ["Random Forest", "Gradient Boosting", "Neural Network", "Logistic Regression"])
            st.slider("Detection Sensitivity", 0.0, 1.0, 0.6)
            st.number_input("Retraining Frequency (days)", value=7)

        with col2:
            st.multiselect("Risk Indicators",
                          ["Low Engagement", "Missing Assignments", "Poor Performance", "Declining Trends", "Infrequent Logins"],
                          default=["Low Engagement", "Missing Assignments", "Poor Performance"])
            st.slider("False Positive Tolerance", 0.0, 1.0, 0.2)

        st.markdown("### Model Monitoring")
        st.checkbox("Enable Performance Logging", value=True)
        st.checkbox("Enable Automated Retraining", value=True)
        st.checkbox("Send Alert on Performance Degradation", value=True)

        st.button("Save AI Settings")

    with tab3:
        st.subheader("Integration Settings")

        st.markdown("### LMS Integration")
        st.selectbox("LMS Type", ["Canvas", "Moodle", "Blackboard", "D2L Brightspace", "Custom"])
        st.text_input("API Endpoint")
        st.text_input("API Key", type="password")
        st.selectbox("Sync Frequency", ["Hourly", "Daily", "Weekly"])
        st.checkbox("Two-way Sync", value=True)

        st.markdown("### Authentication Integration")
        st.checkbox("Enable Single Sign-On (SSO)", value=False)
        st.selectbox("SSO Provider", ["None", "Google", "Microsoft", "Okta", "SAML"])
        st.text_input("SSO Endpoint")
        st.text_input("Client ID")
        st.text_input("Client Secret", type="password")

        st.markdown("### Analytics Integration")
        st.checkbox("Enable Google Analytics", value=False)
        st.text_input("Google Analytics ID")
        st.checkbox("Enable Custom Analytics", value=True)
        st.text_input("Analytics Endpoint")

        st.button("Save Integration Settings")

    with tab4:
        st.subheader("Backup & Maintenance")

        st.markdown("### Automated Backups")
        col1, col2 = st.columns(2)

        with col1:
            st.checkbox("Enable Automated Backups", value=True)
            st.selectbox("Backup Frequency", ["Daily", "Weekly", "Monthly"])
            st.number_input("Retention Period (days)", value=30)

        with col2:
            st.text_input("Backup Location")
            st.checkbox("Enable Encryption", value=True)
            st.checkbox("Enable Compression", value=True)

        st.markdown("### System Maintenance")
        col1, col2 = st.columns(2)

        with col1:
            st.checkbox("Enable Maintenance Mode", value=False)
            st.date_input("Scheduled Maintenance Date")
            st.time_input("Scheduled Maintenance Time")

        with col2:
            st.text_area("Maintenance Message", "System will be undergoing scheduled maintenance...")
            st.number_input("Estimated Downtime (hours)", value=2)

        st.markdown("### System Logs")
        st.selectbox("Log Level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        st.number_input("Log Retention (days)", value=14)
        st.button("Download System Logs")

        st.button("Save Maintenance Settings")
