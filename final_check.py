import sqlite3
import os

db_path = r"c:\Users\User\OneDrive\Documents\Smoky Bites\db_v2.sqlite3"

with open("final_db_check.log", "w") as f:
    if not os.path.exists(db_path):
        f.write(f"ERROR: {db_path} does not exist!\n")
    else:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(orders_order)")
        cols = [c[1] for c in cursor.fetchall()]
        f.write("Columns in orders_order (db_v2):\n")
        f.write("\n".join(cols))
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user'")
        auth_exists = cursor.fetchone()
        f.write(f"\nauth_user exists: {bool(auth_exists)}\n")
        conn.close()
