#!/usr/bin/env python3
"""
Script to extract functions from app.py into separate page files
"""
import re

# Function extraction mappings
EXTRACTIONS = [
    # (function_name, start_line, end_line, output_file, imports_needed)
    ("display_class_management", 341, 449, "code/pages/teacher/class_management.py", ["streamlit as st", "pandas as pd"]),
    ("display_student_progress", 878, 1189, "code/pages/teacher/student_progress.py", ["streamlit as st", "pandas as pd", "numpy as np", "plotly.express as px", "plotly.graph_objects as go"]),
    ("display_content_management", 1400, 1517, "code/pages/teacher/content_management.py", ["streamlit as st", "pandas as pd"]),
    ("display_analytics", 1518, 1857, "code/pages/teacher/analytics.py", ["streamlit as st", "pandas as pd", "numpy as np", "plotly.express as px"]),
    ("display_learning_path", 450, 793, "code/pages/student/learning_path.py", ["streamlit as st", "pandas as pd", "plotly.express as px", "plotly.graph_objects as go", "modules.auth.get_user_preferences", "modules.auth.update_user_preferences"]),
    ("display_student_performance", 794, 877, "code/pages/student/performance.py", ["streamlit as st", "pandas as pd", "plotly.express as px"]),
    ("display_schedule", 1190, 1318, "code/pages/student/schedule.py", ["streamlit as st", "datetime"]),
    ("display_resources", 1319, 1399, "code/pages/student/resources.py", ["streamlit as st", "pandas as pd"]),
]

def extract_function(app_file, func_name, start_line, end_line):
    """Extract function from app.py"""
    with open(app_file, 'r') as f:
        lines = f.readlines()

    # Get function lines (1-indexed to 0-indexed)
    function_lines = lines[start_line-1:end_line]
    return ''.join(function_lines)

def create_page_file(output_file, function_code, imports):
    """Create a page file with imports and function"""
    # Build imports
    import_lines = []
    for imp in imports:
        if " as " in imp:
            import_lines.append(f"import {imp}")
        elif ".":
            parts = imp.split(".")
            if len(parts) == 2:
                import_lines.append(f"from {parts[0]} import {parts[1]}")
            else:
                import_lines.append(f"from {'.'.join(parts[:-1])} import {parts[-1]}")
        else:
            import_lines.append(f"import {imp}")

    imports_block = "\n".join(import_lines)

    # Create file content
    content = f"""# {output_file.split('/')[-1]} - Auto-extracted from app.py
{imports_block}


{function_code}
"""

    # Write file
    with open(output_file, 'w') as f:
        f.write(content)

    print(f"✓ Created {output_file}")

def main():
    app_file = "code/app.py"

    for func_name, start, end, output_file, imports in EXTRACTIONS:
        print(f"Extracting {func_name}...")
        func_code = extract_function(app_file, func_name, start, end)
        create_page_file(output_file, func_code, imports)

    print("\n✓ All functions extracted successfully!")

if __name__ == "__main__":
    main()
