# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a presentation project directory containing both research materials and a Streamlit-based AI-enhanced adaptive learning platform prototype. The project has two main components:

1. **Research Papers and Presentation Materials** ([presentation/](presentation/)): Academic conference presentation materials based on research about data-driven adaptive curriculum personalization for engineering students
2. **Streamlit Application** ([code/](code/)): A working prototype implementing AI-driven personalized learning pathways

## Running the Application

The Streamlit application is located in the [code/](code/) directory.

**Python Version:** 3.11.14

**Installing Dependencies:**
```bash
cd code
source .venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt
```

**Starting the Application:**
```bash
cd code
.venv/bin/streamlit run app.py
# OR after activating venv:
source .venv/bin/activate
streamlit run app.py
```

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

**Important Notes:**
- The virtual environment is located at [code/.venv/](code/.venv/)
- All dependencies are listed in [code/requirements.txt](code/requirements.txt)
- User data is stored in [code/data/users.csv](code/data/users.csv) (auto-created on first run)
- If you encounter import errors, clear cache: `rm -rf .streamlit __pycache__ modules/__pycache__`

## Architecture

### Application Structure

- **[code/app.py](code/app.py)**: Main Streamlit application (1,600+ lines) containing all UI components and page logic
- **[code/modules/auth.py](code/modules/auth.py)**: Authentication system using SHA-256 hashing with CSV-based user storage
- **[code/modules/recommender.py](code/modules/recommender.py)**: Multi-armed bandit implementation using Upper Confidence Bound (UCB) algorithm for content recommendation
- **[code/modules/data_loader.py](code/modules/data_loader.py)**: Data loading utilities
- **[code/jwt_auth.py](code/jwt_auth.py)**: JWT token generation and verification
- **[code/rbac.py](code/rbac.py)**: Role-based access control system
- **[code/session.py](code/session.py)**: Session management with timeout handling

### Data Storage

The application uses CSV files for data persistence:
- User data stored in `data/users.csv` (created automatically on first run)
- OULAD (Open University Learning Analytics Dataset) files in [data/](data/):
  - [studentInfo.csv](data/studentInfo.csv)
  - [studentAssessment.csv](data/studentAssessment.csv)
  - [studentRegistration.csv](data/studentRegistration.csv)
  - [studentVle.csv](data/studentVle.csv) (453MB - virtual learning environment interactions)
  - [assessments.csv](data/assessments.csv)
  - [courses.csv](data/courses.csv)
  - [vle.csv](data/vle.csv)

### Role-Based System

Three user roles with different navigation and permissions:
- **Admin**: User Management, Course Management, System Settings
- **Teacher**: Class Management, Student Progress, Content Management, Analytics
- **Student**: My Learning Path, Performance, Schedule, Resources

## Key Implementation Details

### Multi-Armed Bandit Recommender

The core recommendation engine ([code/modules/recommender.py](code/modules/recommender.py)) implements:
- Upper Confidence Bound (UCB) algorithm for balancing exploration vs exploitation
- Configurable exploration parameter (default 0.2)
- Reward tracking and update mechanism for continuous learning

### Authentication Flow

1. User logs in via [code/app.py](code/app.py) login UI
2. Credentials verified against SHA-256 hash in [code/modules/auth.py](code/modules/auth.py)
3. JWT token generated and stored in session state
4. Session timeout tracked via last_activity timestamp
5. RBAC checks permission for each page access

### Session Management

Sessions automatically expire based on inactivity. The session validation checks run on every page load and will force re-login if expired.

## Research Paper Context

The application implements concepts from the research paper "Data-Driven Adaptive Curriculum-Personalizing Academic Pathways for Enhanced Engineering Student Success" ([presentation/paper/v2_fiee.pdf](presentation/paper/v2_fiee.pdf)).

**Key Research Findings:**
- System reduces "regret" (suboptimal recommendations) by 66% compared to standard approaches
- Uses contextual bandit algorithms for adaptive learning path recommendations
- Addresses student attrition in engineering programs through personalized interventions

**Presentation Materials:**
- [presentation/presentation_guide.md](presentation/presentation_guide.md): Meta-guide on creating effective academic presentations
- [presentation/diagram_guides.md](presentation/diagram_guides.md): ASCII art blueprints for presentation diagrams
- [presentation/presentation_v1.md](presentation/presentation_v1.md): First version of presentation
- [presentation/presentation_v2.md](presentation/presentation_v2.md): Second version of presentation
- [presentation/presentation_with_code.md](presentation/presentation_with_code.md): Technical presentation with code examples
- [code/docs/AI-Enhanced Adaptive Learning Platform.md](code/docs/AI-Enhanced Adaptive Learning Platform.md): Complete technical specification

## Development Notes

### Data Handling
The OULAD dataset contains real anonymized student data from Open University. The [studentVle.csv](data/studentVle.csv) file is particularly large (453MB) and contains fine-grained interaction logs.

### Security Considerations
- Authentication uses SHA-256 (note: production should use bcrypt or similar)
- JWT tokens for session management
- Role-based access control enforced at page level
- CSV-based storage is for prototype only; production requires proper database

### UI Pattern
The app follows a single-file Streamlit pattern where all pages are functions within [app.py](app.py). Each display function (e.g., `display_dashboard()`, `display_learning_path()`) handles a specific navigation page.
