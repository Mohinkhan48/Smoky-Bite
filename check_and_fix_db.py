import sqlite3
import os

with open('db_fix.log', 'w') as log:
    def log_print(msg):
        print(msg)
        log.write(msg + '\n')

    db_path = 'db_v2.sqlite3'
    if not os.path.exists(db_path):
        log_print(f"ERROR: {db_path} not found")
        exit(1)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check columns in orders_order
    cursor.execute("PRAGMA table_info(orders_order)")
    columns = [row[1] for row in cursor.fetchall()]

    log_print("Columns in orders_order:")
    for col in columns:
        log_print(f" - {col}")

    # Check if customer_name is missing
    if 'customer_name' not in columns:
        log_print("FIXING: Adding customer_name column...")
        cursor.execute("ALTER TABLE orders_order ADD COLUMN customer_name VARCHAR(100) DEFAULT 'Guest'")
        conn.commit()
        log_print("FIXED: customer_name column added.")
    else:
        log_print("OK: customer_name column exists.")

    # Check auth_user table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user'")
    auth_exists = cursor.fetchone()
    if auth_exists:
        log_print("OK: auth_user table exists.")
    else:
        log_print("ERROR: auth_user table is MISSING!")

    conn.close()
