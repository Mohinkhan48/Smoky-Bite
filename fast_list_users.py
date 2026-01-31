import sqlite3
import os

dbs = ['db.sqlite3', 'db_v2.sqlite3', 'db_v3.sqlite3']

for db_name in dbs:
    if not os.path.exists(db_name):
        continue
    print(f"\n--- DATABASE: {db_name} ---")
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT username, is_superuser, is_staff, is_active FROM auth_user")
        rows = cursor.fetchall()
        for row in rows:
            print(f"User: '{row[0]}' | Super: {row[1]} | Staff: {row[2]} | Active: {row[3]}")
        conn.close()
    except Exception as e:
        print(f"Error reading {db_name}: {e}")
