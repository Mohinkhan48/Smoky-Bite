import os

content = """#!/usr/bin/env bash
# Exit on error
set -o errexit

# Run migrations at startup
python manage.py migrate

# Start Gunicorn
gunicorn smoky_bites.wsgi:application
"""

# Force LF line endings for Linux compatibility
with open('render_start.sh', 'wb') as f:
    f.write(content.replace('\r\n', '\n').encode('utf-8'))

print("Successfully wrote render_start.sh with LF line endings.")
