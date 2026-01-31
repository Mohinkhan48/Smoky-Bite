
@echo off
echo STARTING DEBUG > debug_log.txt
python manage.py makemigrations orders >> debug_log.txt 2>&1
python manage.py migrate >> debug_log.txt 2>&1
python populate.py >> debug_log.txt 2>&1
echo DONE >> debug_log.txt
