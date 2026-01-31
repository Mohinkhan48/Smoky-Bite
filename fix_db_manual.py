import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

def check_structure():
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(orders_order)")
        columns = cursor.fetchall()
        print("Columns in orders_order:")
        for col in columns:
            print(f" - {col[1]}")
        
        column_names = [col[1] for col in columns]
        if 'customer_name' not in column_names:
            print("\n!!! customer_name is MISSING. Attempting manual fix...")
            try:
                cursor.execute("ALTER TABLE orders_order ADD COLUMN customer_name varchar(100) DEFAULT 'Guest' NOT NULL")
                print("Successfully added customer_name via manual SQL.")
            except Exception as e:
                print(f"Failed to add column: {e}")
        else:
            print("\ncustomer_name ALREADY EXISTS.")

        # Also check length of order_id
        # In SQLite we can't easily change length without recreating, but usually VARCHAR length is ignored anyway
        # but let's check if we can insert a long one.
        
if __name__ == "__main__":
    check_structure()
