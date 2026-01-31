#!/usr/bin/env bash
# Exit on error
set -o errexit

# Run migrations at startup (Mandatory for SQLite on Render)
python manage.py migrate

# Start Gunicorn
gunicorn smoky_bites.wsgi:application
