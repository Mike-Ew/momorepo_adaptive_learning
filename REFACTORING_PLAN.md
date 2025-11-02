# App.py Refactoring Plan

## Current Structure (2007 lines)
Single monolithic `app.py` file with all pages and logic combined.

## Target Structure
```
code/
├── app.py (main entry point - ~200 lines)
├── pages/
│   ├── __init__.py
│   ├── common/
│   │   ├── __init__.py
│   │   └── dashboard.py ✓
│   ├── admin/
│   │   ├── __init__.py
│   │   ├── user_management.py
│   │   └── system_settings.py
│   ├── teacher/
│   │   ├── __init__.py
│   │   ├── class_management.py
│   │   ├── student_progress.py
│   │   ├── content_management.py
│   │   └── analytics.py
│   └── student/
│       ├── __init__.py
│       ├── learning_path.py
│       ├── performance.py
│       ├── schedule.py
│       └── resources.py
└── modules/ (existing)
```

## Page Mapping

### Common Pages (used by multiple roles)
- `dashboard.py` - Dashboard (all roles) ✓ DONE

### Admin Pages
- `user_management.py` - display_user_management()
- `system_settings.py` - display_system_settings()

### Teacher Pages
- `class_management.py` - display_class_management()
- `student_progress.py` - display_student_progress()
- `content_management.py` - display_content_management()
- `analytics.py` - display_analytics()

### Student Pages
- `learning_path.py` - display_learning_path()
- `performance.py` - display_student_performance()
- `schedule.py` - display_schedule() (student portion)
- `resources.py` - display_resources()

## Implementation Steps

1. ✓ Create directory structure
2. ✓ Extract dashboard (common)
3. Extract admin pages
4. Extract teacher pages
5. Extract student pages
6. Update main app.py to import from pages
7. Test each page
8. Commit to git

## Benefits
- Better code organization
- Easier to maintain and debug
- Faster development (work on specific pages)
- Reduced merge conflicts in team settings
- Better separation of concerns
