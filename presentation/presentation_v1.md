# Data-Driven Adaptive Curriculum & Personalized Enhanced Student Success

**David Mike-Ewewie, et al.**

Department of Computer Science, The University of Texas Permian Basin

---

## The Problem: Rigid Curricula

- **One-Size-Fits-All:** Traditional academic pathways don't adapt to individual student needs, learning paces, or personal circumstances.
- **High Risk:** Students who face challenges (academic or personal) can easily fall behind with no clear path to recovery.
- **Wasted Potential:** We are missing opportunities to maximize student engagement and success by not leveraging available data.

---

## The Vision: A Dynamic, Personalized Framework

A data-driven system that:
- **Continuously Learns:** Uses student data (analytics, health, psychometrics) to understand what works.
- **Adapts in Real-Time:** Adjusts curriculum, pacing, and schedules automatically.
- **Proactively Supports:** Detects early signs of academic risk (e.g., ADHD, anxiety, emergencies) and provides tailored interventions.

---

## Core Concept: A Sequential Decision Process

We model a student's academic journey as a sequence of decisions.

- **At each step (e.g., a new semester):**
    - The system observes the student's current state.
    - It recommends an action (a set of courses).
    - It receives a reward (the student's performance and engagement).
- **Goal:** Maximize the cumulative, long-term reward for the student.

---

## Why Multi-Armed Bandits (MAB)?

The MAB framework is ideal for balancing two critical needs:

- **Exploitation:** Recommending courses that we are confident will lead to good outcomes based on past data.
- **Exploration:** Recommending new or less-certain courses to discover potentially high-value learning paths.

This allows the system to continuously improve its recommendations.

---

## The Proposed Framework

1.  **Data Integration & Student Modeling:**
    - Aggregate diverse data (academic history, demographics, preferences) into a multi-dimensional student profile.

2.  **Contextual Bandits for Personalization:**
    - The "context" is the student's profile. The system learns the best action not just overall, but for a student *like this*.

3.  **Algorithmic Core: Thompson Sampling:**
    - An effective algorithm that naturally balances the explore-exploit tradeoff by using probability distributions to model the expected success of each course.

---

## Algorithmic Workflow

```
Initialize Bandit Model for all courses with prior beliefs

for each student:
  for each decision point (semester):
    1. Observe student's current state (profile)
    2. Determine available courses (action space)
    3. Sample a potential outcome from each course's belief model
    4. Select the course with the best sampled outcome
    5. Recommend the course
    6. Observe the actual outcome (grade, engagement)
    7. Update the belief model for the chosen course
```

---

## Handling Real-World Complexity

- **Multiple Courses:** Handle simultaneous recommendations by treating a set of courses as a single "composite" action or by selecting courses sequentially.
- **Constraints:** Integrate hard constraints like prerequisites, credit limits, and degree requirements to ensure all pathways are valid.

---

## Scalability & Generality

- **Efficiency:** Bandit algorithms are computationally lightweight and can scale to thousands of students and courses.
- **Domain-Agnostic:** The framework can be adapted to different programs (STEM, Humanities, K-12) by changing the reward function and constraints.
- **Cold-Start Problem:** For new students or courses, the system can default to expert-defined curricula and personalize as data is collected.

---

## Discussion & Future Work

- **Trust and Transparency:** Recommendations must be explainable to gain trust from students and advisors.
- **Ethical Implications:** We must actively work to prevent the system from reinforcing existing biases present in historical data.
- **Human-in-the-Loop:** The framework is envisioned as a decision-support tool for advisors, not a replacement.
- **Next Step:** Conduct a pilot study with undergraduate engineering students to empirically validate the model.

---

## Conclusion

- We have presented a theoretical framework for a novel data-driven system to dynamically personalize academic pathways.
- By leveraging a contextual multi-armed bandit approach, we can continuously learn from student outcomes to maximize engagement and success.
- This work lays the foundation for a more responsive and student-centered educational experience.

---

## Questions?
