import sqlite3
import sys

with open('db_status.txt', 'w') as f:
    try:
        conn = sqlite3.connect('db_v2.sqlite3')
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(orders_order)")
        columns = cursor.fetchall()
        found = False
        for col in columns:
            f.write(str(col) + '\n')
            if col[1] == 'customer_number':
                found = True
        
        if found:
            f.write("SUCCESS: customer_number column exists.\n")
        else:
            f.write("FAILURE: customer_number column missing.\n")
        conn.close()
    except Exception as e:
        f.write(f"ERROR: {e}\n")
