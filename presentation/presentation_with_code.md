# Data-Driven Adaptive Curriculum: Personalizing Academic Pathways for Enhanced Engineering Student Success

**David Mike-Ewewie, et al.**

Department of Computer Science, The University of Texas Permian Basin

---

## The Problem: The Engineering "Leaky Funnel"

- **High Attrition:** Engineering programs lose nearly half their students. Only 52% of first-time majors graduate within six years.
- **Rigid Pathways:** The core issue is the rigid prerequisite chain. A single failure in a gateway course like Calculus I can cause a year-long delay, dramatically increasing the risk of attrition.
- **Visualizing the Problem:**

    - *(Presenter should show Diagram 1: The Leaky Funnel)*
    - This diagram illustrates how a 28% D/F/W rate in Calculus I can ripple through the entire degree plan, pushing back critical courses and putting students at risk.

---

## Our Solution: An Adaptive Recommendation System

- **The Vision:** A system that personalizes course sequences for first-year engineering students, navigating around bottlenecks while respecting all ABET accreditation requirements.
- **The Engine:** We use a **Contextual Multi-Armed Bandit**, an algorithm that learns and adapts to each student's unique situation.
- **The Goal:** To provide the right course, to the right student, at the right time.

---

## How It Works: The Adaptive Feedback Loop

- *(Presenter should show Diagram 3: The Adaptive Feedback Loop)*
- **1. Assess Context:** We build a 12-dimensional profile for each student, capturing their academic history, demographics, and real-time engagement on the learning platform.
- **2. Recommend:** The bandit algorithm, using a technique called **Thompson Sampling**, recommends the optimal course. It balances "exploiting" paths that have worked for similar students in the past with "exploring" new paths that might be even better.
- **3. Co-Plan & Monitor:** The recommendation is a starting point for a conversation between the student and their advisor. We continuously monitor engagement to catch problems early.
- **4. Learn & Audit:** Every outcome teaches the system. We update our models and constantly audit for fairness to ensure our recommendations are equitable.

---

## The "Brain" of the System: The Student Context Vector

- *(Presenter should show Diagram 2: The Student Context Vector)*
- **Rich Data:** Our system doesn't just look at grades. It combines three types of signals:
    - **Demographics:** To understand the student's background.
    - **Academic History:** To understand their academic preparation.
    - **Engagement Signals:** Real-time data like VLE clicks and forum posts to see how they're doing *right now*.
- **Privacy-Preserving:** All data is handled in a FERPA-compliant way, with differential privacy to protect student identities.

---

## Live Demo: The Adaptive Learning Platform

- **From Theory to Practice:** To demonstrate how this system works in a real-world scenario, I'm going to show you a prototype of the platform built with Streamlit.
- **What you're seeing:** This is a live application that brings together all the concepts we've discussed. It has different views for students, teachers, and administrators.
- **(Presenter opens the Streamlit App)**
    - **Student View:**
        - Log in as a student.
        - Navigate to "My Learning Path".
        - **Point out the personalized recommendations:** "Here you can see the system is recommending specific modules and resources based on this student's progress and learning style. This is the contextual bandit in action."
        - Show the "Performance" dashboard, highlighting how the student can track their own progress.
    - **Teacher View:**
        - Log out and log in as a teacher.
        - Go to "Student Progress".
        - **Highlight the at-risk student identification:** "The dashboard gives teachers a quick overview of their class, and flags students who might be struggling. This allows for early interventions."
        - Click on an individual student to show the detailed view. "The teacher can then drill down to see a specific student's activity and provide targeted support."

---

## The Results: A Clear Improvement

- *(Presenter should show Diagram 4: The Result - A Clear Improvement)*
- **Reduced "Regret":** Our system reduced suboptimal course recommendations by **66%** compared to a standard popularity-based approach. This means students are twice as likely to get a course that is right for them.
- **High Precision:** The system's top-3 recommendations included the student's actual final choice nearly 50% of the time, providing actionable guidance for advisors.
- **Fairness:** We audited the system for fairness across gender groups and found a negligible difference in recommendation quality (a gap of only 0.006, well below our target of 0.02).
- **Scalable:** The system is fast, handling over 500 requests per second on modest hardware, making it ready for real-world deployment.

---

## The "Money Chart": Cumulative Regret

- *(Presenter should show the "Cumulative Simple-Regret" graph from Figure 3 of the paper)*
- **The Story:** This graph tells the whole story. The top line is the baseline—what happens when you just recommend the most popular courses. The bottom line is our bandit.
- **The Takeaway:** You can see that our system quickly learns from its recommendations, diverging from the baseline and consistently making better choices. The flat slope at the end shows it has converged on an effective, personalized policy.

---

## Conclusion & Future Work

- **What We've Done:** We've built and validated a data-driven system that can personalize academic pathways, significantly improving on static, one-size-fits-all approaches.
- **The Impact:** This work provides a practical, scalable, and fair tool to help universities address the persistent challenge of engineering student attrition.
- **Next Steps:**
    - A pilot study with 120 engineering students is planned for Spring 2026.
    - We will develop an advisor dashboard to make the system's recommendations transparent and interpretable.
    - We will explore more advanced models to capture even more nuanced student states.

---

## Questions?
