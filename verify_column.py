import sqlite3

def check_column():
    conn = sqlite3.connect('db_v2.sqlite3')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(orders_order)")
    columns = cursor.fetchall()
    found = False
    for col in columns:
        print(col)
        if col[1] == 'customer_number':
            found = True
    
    if found:
        print("SUCCESS: customer_number column exists.")
    else:
        print("FAILURE: customer_number column missing.")
    conn.close()

if __name__ == "__main__":
    check_column()
