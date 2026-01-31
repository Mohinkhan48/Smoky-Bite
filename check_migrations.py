import sqlite3
import os

with open('migration_check.log', 'w') as log:
    db_path = 'db_v2.sqlite3'
    if not os.path.exists(db_path):
        log.write(f"ERROR: {db_path} not found\n")
        exit(1)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT app, name FROM django_migrations WHERE app='orders'")
        migrations = cursor.fetchall()
        log.write("Applied migrations for 'orders':\n")
        for app, name in migrations:
            log.write(f" - {name}\n")
    except Exception as e:
        log.write(f"ERROR: {str(e)}\n")

    conn.close()
