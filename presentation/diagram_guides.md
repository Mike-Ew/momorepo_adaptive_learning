# Presentation Diagram Guides

This file contains text-based drafts for the key visuals in your presentation. Use these as a blueprint for creating the final graphics.

---

### Diagram 1: The Problem - The Leaky Funnel

**Purpose:** To visually represent the high attrition rate in engineering programs.

```
/=======================================\
| 100 First-Year Engineering Entrants    |
| (National 6-year completion ~52%)      |
\=======================================/
                   ||
                   vv
        +-------------------------------+
        | Calculus I (Gateway Bottleneck)|
        | National D/F/W ~28% [Section I]|
        +-------------------------------+
                   ||
                   vv
        /===============================\
        | ~72 advance after year-long   |
        | delay to Calculus II / Physics|
        \===============================/
                   ||
                   vv
        +-------------------------------+
        | Physics I -> Statics chain    |
        | ABET plans allow little slack |
        +-------------------------------+
                   ||
                   vv
        /===============================\
        | ~52 finish within six years   |
        | if early gates are cleared    |
        \===============================/
                   ||
                   vv
        +-------------------------------+
        | Early failures add extra year |
        | cost, raising attrition risk  |
        +-------------------------------+
```

**Explainer:**  

- National six-year completion for first-time engineering majors is ~52 percent, per `v2_fiee.pdf` Section I.  
- Calculus I carries a 28 percent D/F/W rate in the cited MAA study, so it is the primary leak in the funnel.  
- ABET degree plans require 128-135 credits, leaving little slack; failing Fall Calculus I pushes Physics I and Statics back a year, which raises attrition and tuition risk.  
- The diagram illustrates why adaptive sequencing is needed: a single early failure removes nearly half the cohort without targeted intervention.

---

### Diagram 2: The Input - Student Context Vector

**Purpose:** To show the rich, multi-dimensional data you use for each student.

```
                  Demographics                   Academic History             Engagement Signals
                  -------------                   ----------------             -------------------
                  [ Gender Identity ]            [ Prior GPA z-score ]        [ Weekly VLE Clicks  ]
                        |                                   |                          |
                  [ Age Band ]                       [ Cumulative Credits ]      [ Forum Post Count ]
                        |                                   |                          |
                  [ Highest Prior Education ]       [ Failed Module Count ]      [ Quiz Submission Count ]
                        |                                   |                          |
                  [ Socio-Economic Band ]           [ Weeks Since Last Enrollment ]         |
                        |                                   |                              |
                  [ Disability Flag ]                       |                              v
                        |                                   v                      [ Engagement Pulse ]
                        v                              [ Performance Log ]                   |
                  [ Demographic Span ]                         |                              |
                        \                                      |                              /
                         \                                     |                             /
                          \                                    |                            /
                           +----------------------------------+----------------------------+
                           |          STUDENT CONTEXT HUB (Feature Aggregation)           |
                           +----------------------------------+----------------------------+
                                                               |
                                                               v
                                                 +-------------------------------+
                                                 | Context Vector (Student State) |
                                                 | Normalized & Time-Aware        |
                                                 +------------------+------------+
                                                                    |
                                                                    v
                                                 +-------------------------------+
                                                 | Contextual Bandit Algorithm   |
                                                 | Generates Course Recommendation|
                                                 +------------------+------------+
                                                                    |
                                                                    v
                                                 +-------------------------------+
                                                 | Advisor + Student Action Plan |
                                                 +-------------------------------+
```

**Explainer:**

- **Demographics** includes the five attributes enumerated in `v2_fiee.pdf` Section III-D: gender identity, age-band, highest prior education, socio-economic band, and disability flag, so the system captures equity-relevant cues without exposing raw identifiers.
- **Academic History** mirrors the paper's longitudinal features: prior GPA (z-normalized), cumulative credits earned, previously failed modules, and weeks since last enrollment. These help the bandit estimate readiness and recovery needs.
- **Engagement Signals** represent the three dynamic VLE metrics in the study: weekly click activity, forum participation, and quiz submission cadence, which are early indicators of academic momentum.
- The **Student Context Hub** reflects the FERPA-compliant pipeline described in Section III-B, where nightly ETL jobs ingest registrar, LMS, and survey feeds before normalization. The resulting 12-dimensional context vector powers the contextual Thompson-sampling bandit, and recommendations are finalized with advisor and student input as outlined in Section IV.

---

### Diagram 3: The Engine - The Adaptive Feedback Loop

**Purpose:** To explain how your system works in a simple, cyclical way.

```
      +---------------------------------------------------+
      | (1) ASSESS CONTEXT                               |
      | Nightly ETL -> 12-dim vector (Sections III-B/D)  |
      | Demographic, history, VLE signals                |
      +---------------------------+----------------------+
                                  |
                                  v
      +---------------------------+----------------------+
      | (2) FILTER & RECOMMEND                          |
      | Enforce prereq / credit rules (ABET constraints)|
      | Contextual Thompson Sampling ranks options      |
      +---------------------------+----------------------+
                                  |
                                  v
      +---------------------------+----------------------+
      | (3) CO-PLAN & MONITOR                          |
      | Advisor + student review recommendation         |
      | Weekly VLE checks flag engagement dips         |
      +---------------------------+----------------------+
                                  |
                                  v
      +---------------------------+----------------------+
      | (4) LEARN & AUDIT                               |
      | Update Bayesian posterior with outcomes         |
      | Track regret + fairness gap (delta=0.006)       |
      +---------------------------^----------------------+
                                  |
                                  +----- feedback into ASSESS -----+
```

**Explainer:**

- Step 1 matches the FERPA-safe pipeline and 12-feature context vector described in Sections III-B and III-D.  
- Step 2 depicts the action filtering plus contextual Thompson Sampling flow covered in Sections III-F and III-G, guaranteeing ABET compliance.  
- Step 3 reflects the advisor-in-the-loop process and weekly engagement monitoring discussed in Section IV-D and illustrated by Fig. 2.  
- Step 4 captures the Bayesian update and fairness audit (gender regret gap of 0.006) reported in Sections III-G and IV-B, closing the adaptive loop.

---

### Diagram 4: The Result - A Clear Improvement

**Purpose:** To provide a simple, memorable visual of your main result.

```
                OUTCOME SNAPSHOT (Section IV)

+------------------------------+-----------------+------------------------+
| Metric                       | Popularity      | Bandit (This Work)     |
+------------------------------+-----------------+------------------------+
| Regret per student (lower)   | 0.879           | 0.577  (~66% drop)     |
| Precision@3 (higher)         | 0.344           | 0.488  (+42%)          |
| MAE vs pass outcome (lower)  | 0.450 (LogReg)  | 0.423 (within 6%)      |
| Fairness gap |delta_regret|  | -               | 0.006  (< 0.02 target) |
| Throughput (t3.medium)       | -               | 520 req/s @ 38 ms      |
+------------------------------+-----------------+------------------------+

Key takeaway: contextual Thompson Sampling halves misaligned
recommendations while remaining fast and equitable.
```

**Explainer:**

- Regret, Precision@3, and MAE values are reported in Table III and Section IV, showing the bandit rivals logistic regression while beating popularity heuristics.  
- The fairness gap of 0.006 comes from Section IV-B, staying well under the 0.02 threshold for gender equity.  
- Throughput metrics (520 req/s with 38 ms latency) are from Section IV-C, demonstrating production readiness on modest hardware.  
- Presenting the metrics side-by-side reinforces that the adaptive system simultaneously improves accuracy, equity, and scalability.
