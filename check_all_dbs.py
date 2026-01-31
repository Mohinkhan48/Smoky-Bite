import sqlite3
import glob
import os

def check_db(path):
    print(f"--- Checking {path} ---")
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders_category';")
        if not cursor.fetchone():
            print("  Table 'orders_category' not found.")
            conn.close()
            return

        cursor.execute("SELECT name, COUNT(*) FROM orders_category GROUP BY name HAVING COUNT(*) > 1;")
        dupes = cursor.fetchall()
        
        if dupes:
            print(f"  FOUND DUPLICATES:")
            for name, count in dupes:
                print(f"    - '{name}': {count} copies")
        else:
            print("  No duplicates found in Category table.")
            
        conn.close()
    except Exception as e:
        print(f"  Error reading DB: {e}")

def scan():
    files = glob.glob("*.sqlite3")
    for f in files:
        check_db(f)

if __name__ == "__main__":
    scan()
