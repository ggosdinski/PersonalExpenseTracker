import sqlite3

DB_NAME = "expenses.db"

# ---------------------------
# Database Connection
# ---------------------------
def create_connection(db_file=DB_NAME):
    """Create a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error creating connection: {e}")
        return None


# ---------------------------
# Category Operations
# ---------------------------
def initialize_categories(conn):
    fixed_categories = [
        "Donations",
        "Rent",
        "Travel",
        "Hobbies",
        "Food",
        "Health"
    ]
    cursor = conn.cursor()
    for category in fixed_categories:
        try:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (category,))
        except sqlite3.IntegrityError:
            # Ignore if category already exists
            pass
    conn.commit()


def add_category(conn, name):
    """Add a new category to the database."""
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        print("Category added successfully.")
    except sqlite3.IntegrityError:
        print("Category already exists.")


def get_categories(conn):
    """Return all categories."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories")
    return cursor.fetchall()


def update_category(conn, category_id, new_name):
    """Update the name of a category by ID."""
    cursor = conn.cursor()
    cursor.execute("UPDATE categories SET name = ? WHERE id = ?", (new_name, category_id))
    conn.commit()
    print("Category updated successfully.")


def delete_category(conn, category_id):
    """Delete a category by ID."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    conn.commit()
    ## print("Category deleted successfully.")


# ---------------------------
# Transaction Operations
# ---------------------------
def add_transaction(conn, amount, date, category_id, description, type_):
    """Add a new transaction (income or expense)."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (amount, date, category_id, description, type)
        VALUES (?, ?, ?, ?, ?)
    """, (amount, date, category_id, description, type_))
    conn.commit()
    print("Transaction added successfully.")


def get_all_transactions(conn):
    """Retrieve all transactions with category names."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, t.amount, t.date, c.name AS category, t.description, t.type
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        ORDER BY t.date DESC
    """)
    return cursor.fetchall()


def update_transaction(conn, transaction_id, amount=None, date=None, category_id=None, description=None, type_=None):
    """
    Update fields of an existing transaction by ID.
    Only fields provided (not None) will be updated.
    """
    fields = []
    values = []

    if amount is not None:
        fields.append("amount = ?")
        values.append(amount)
    if date is not None:
        fields.append("date = ?")
        values.append(date)
    if category_id is not None:
        fields.append("category_id = ?")
        values.append(category_id)
    if description is not None:
        fields.append("description = ?")
        values.append(description)
    if type_ is not None:
        fields.append("type = ?")
        values.append(type_)

    if not fields:
        print("No fields to update.")
        return

    values.append(transaction_id)
    sql = f"UPDATE transactions SET {', '.join(fields)} WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    print("Transaction updated successfully.")


def delete_transaction(conn, transaction_id):
    """Delete a transaction by ID."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    print("Transaction deleted successfully.")

def delete_all_transactions(conn):
    """Delete all transactions from the database."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions")
    conn.commit()
    ## print("All transactions deleted successfully.")

# ---------------------------
# Transaction Queries
# ---------------------------
def get_transactions_by_date_range(conn, start_date, end_date):
    """
    Retrieve transactions between start_date and end_date inclusive.
    Dates must be 'YYYY-MM-DD' strings.
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, t.amount, t.date, c.name AS category, t.description, t.type
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.date BETWEEN ? AND ?
        ORDER BY t.date DESC
    """, (start_date, end_date))
    return cursor.fetchall()


def get_total_expense_by_category(conn):
    """
    Calculate total expenses grouped by category.
    Only considers transactions where type = 'expense'.
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.name AS category, SUM(t.amount) AS total_expense
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.type = 'expense'
        GROUP BY c.name
        ORDER BY total_expense DESC
    """)
    return cursor.fetchall()
