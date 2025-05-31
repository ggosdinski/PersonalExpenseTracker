""" import sqlite3

conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Listar tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Listar columnas de cada tabla
for table in tables:
    print(f"\nColumns in table {table[0]}:")
    cursor.execute(f"PRAGMA table_info({table[0]})")
    columns = cursor.fetchall()
    for col in columns:
        print(col)

conn.close()
 """

""" BORRAR UNA CATEGORIA
from db_operations import create_connection

def delete_category_by_name(conn, name):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE name = ?", (name,))
    conn.commit()
    print(f"Category '{name}' deleted.")

if __name__ == "__main__":
    conn = create_connection("expenses.db")
    delete_category_by_name(conn, "Food")
    conn.close()
 """

import sqlite3
def delete_all_categories(conn):
    """Delete all categories at once."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories")
    conn.commit()
    print("All categories deleted successfully.")
