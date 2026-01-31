import sqlite3
import os

with open('all_tables.log', 'w') as log:
    db_path = 'db_v2.sqlite3'
    if not os.path.exists(db_path):
        log.write(f"ERROR: {db_path} not found\n")
        exit(1)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    log.write("Tables in DB:\n")
    for t in tables:
        log.write(f" - {t}\n")

    conn.close()
