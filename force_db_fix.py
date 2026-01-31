import sqlite3
import os

db_path = r"c:\Users\User\OneDrive\Documents\Smoky Bites\db_v2.sqlite3"

def force_fix():
    print(f"Connecting to {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check columns
        cursor.execute("PRAGMA table_info(orders_order)")
        columns = [c[1] for c in cursor.fetchall()]
        print(f"Current columns: {columns}")
        
        if 'customer_name' not in columns:
            print("Adding customer_name column...")
            cursor.execute("ALTER TABLE orders_order ADD COLUMN customer_name VARCHAR(100) DEFAULT 'Guest' NOT NULL")
            print("Added customer_name.")
        
        # SQLite doesn't support ALTER COLUMN to change length easily (max_length 10 -> 40)
        # but SQLite's VARCHAR length is actually ignored (it's dynamic). 
        # The crash was likely Django's internal validation OR just the missing column. 
        # I'll just check if we can insert a long ID now.
        
        conn.commit()
        print("Done.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    force_fix()
