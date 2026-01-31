import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

with open('migration_result.log', 'w') as log:
    try:
        log.write("Starting migrations...\n")
        call_command('migrate', no_input=True)
        log.write("Migrations complete.\n")
    except Exception as e:
        log.write(f"ERROR: {str(e)}\n")
