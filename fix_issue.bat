@echo off
echo Starting fix for MultipleObjectsReturned error...

echo 1. Running deduplication script...
venv\Scripts\python.exe deduplicate.py

echo 2. Creating migrations...
venv\Scripts\python.exe manage.py makemigrations orders

echo 3. Applying migrations...
venv\Scripts\python.exe manage.py migrate

echo Fix complete! Please restart your server if it is running.
pause
