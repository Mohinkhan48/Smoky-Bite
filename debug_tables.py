import sqlite3
import os

db_path = r"c:\Users\User\OneDrive\Documents\Smoky Bites\db_v3.sqlite3"

def debug_db():
    if not os.path.exists(db_path):
        print(f"ERROR: {db_path} does not exist!")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"Tables in {db_path}:")
    for t in tables:
        print(f" - {t}")
    conn.close()

if __name__ == "__main__":
    debug_db()
