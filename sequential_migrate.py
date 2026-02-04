import os
import django
from django.core.management import call_command
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

def get_unapplied_migrations():
    from django.db.migrations.executor import MigrationExecutor
    executor = MigrationExecutor(connection)
    pending = executor.migration_plan(executor.loader.graph.leaf_nodes())
    return pending

print("Checking for unapplied migrations...")
pending = get_unapplied_migrations()

if not pending:
    print("No migrations to apply.")
else:
    print(f"Found {len(pending)} pending migrations.")
    for migration, backwards in pending:
        print(f"Applying {migration}...")
        try:
            # We can't easily apply one by one using call_command('migrate') 
            # for a specific migration object, but we can target the app and name.
            app_label = migration.app_label
            migration_name = migration.name
            call_command('migrate', app_label, migration_name, interactive=False)
            print(f"Successfully applied {migration_name}")
        except Exception as e:
            print(f"Error applying {migration}: {e}")
            break
