import sqlite3

db_path = 'db_v2.sqlite3'
print(f"Connecting to {db_path}...")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if column exists
    cursor.execute("PRAGMA table_info(orders_order)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'customer_number' in columns:
        print("Column 'customer_number' already exists.")
    else:
        print("Adding column 'customer_number'...")
        cursor.execute("ALTER TABLE orders_order ADD COLUMN customer_number varchar(15)")
        conn.commit()
        print("SUCCESS: Column added.")
        
except Exception as e:
    print(f"ERROR: {e}")
finally:
    conn.close()
