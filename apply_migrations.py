import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

print("Checking migrations...")
try:
    call_command('migrate', interactive=False)
    print("Migrations applied successfully!")
except Exception as e:
    print(f"Error applying migrations: {e}")
