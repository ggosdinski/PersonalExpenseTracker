from db_operations import (
    create_connection,
    initialize_categories,
    get_categories,
    add_category,
    add_transaction,
    update_transaction,
    delete_transaction,
    delete_all_transactions,
    get_all_transactions,
    get_transactions_by_date_range,
    get_total_expense_by_category
)

def print_menu():
    print("\n=== Personal Expense Tracker ===")
    print("1. View all transactions")
    print("2. Add a transaction")
    print("3. Update a transaction")
    print("4. Delete a transaction")
    print("5. View transactions by date range")
    print("6. View total expense by category")
    print("7. Delete all transactions")
    print("0. Exit")

def add_transaction_flow(conn):
    categories = get_categories(conn)
    if not categories:
        print("No categories found. You need to add a new category first.")
        new_cat = input("Enter new category name: ").strip()
        if new_cat:
            add_category(conn, new_cat)
            categories = get_categories(conn)
        else:
            print("Category name cannot be empty. Returning to main menu.")
            return

    print("Available categories:")
    for idx, cat in enumerate(categories, start=1):
        print(f"{idx}. {cat[1]}")

    try:
        amount = float(input("Enter amount: "))
        date = input("Enter date (YYYY-MM-DD): ").strip()
        description = input("Enter description: ").strip()

        trans_type_input = input("Enter type (I = income, E = expense): ").strip().upper()
        if trans_type_input == "I":
            trans_type = "income"
        elif trans_type_input == "E":
            trans_type = "expense"
        else:
            print("Invalid type. Please enter 'I' or 'E'.")
            return

        selected_index = int(input("Select category by number: "))
        if not 1 <= selected_index <= len(categories):
            print("Invalid category selection. Transaction cancelled.")
            return

        category_id = categories[selected_index - 1][0]
        add_transaction(conn, amount, date, category_id, description, trans_type)
        print("Transaction added successfully!")

    except Exception as e:
        print(f"Error adding transaction: {e}")

def main():
    conn = create_connection("expenses.db")
    ## initialize_categories(conn)

    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            transactions = get_all_transactions(conn)
            if transactions:
                print(f"\n{'ID':<5} {'Amount':<10} {'Date':<12} {'Category':<15} {'Description':<20} {'Type':<10}")
                print("-" * 75)
                for t in transactions:
                    print(f"{t[0]:<5} {t[1]:<10.2f} {t[2]:<12} {t[3]:<15} {t[4]:<20} {t[5]:<10}")
            else:
                print("No transactions found.")

        elif choice == "2":
            add_transaction_flow(conn)

        elif choice == "3":
            try:
                transaction_id = int(input("Enter transaction ID to update: "))
                print("Enter new values (leave blank to keep current):")
                amount_str = input("New amount: ").strip()
                date = input("New date (YYYY-MM-DD): ").strip()
                description = input("New description: ").strip()
                trans_type = input("New type (expense/income): ").strip().lower()

                # Obtener transacción existente
                transactions = get_all_transactions(conn)
                transaction = next((t for t in transactions if t[0] == transaction_id), None)
                if not transaction:
                    print(f"Transaction ID {transaction_id} not found.")
                    return

                # Campos existentes por índice
                # t = (id, amount, date, category_name, description, type)
                amount = float(amount_str) if amount_str else transaction[1]
                date = date if date else transaction[2]
                description = description if description else transaction[4]
                type_val = trans_type if trans_type in ("expense", "income") else transaction[5]

                # Obtener el ID de la categoría actual desde la BD
                cursor = conn.cursor()
                cursor.execute("SELECT category_id FROM transactions WHERE id = ?", (transaction_id,))
                result = cursor.fetchone()
                if result is None:
                    print("Error: Could not find category ID for the transaction.")
                    return
                category_id = result[0]  # Usar el ID existente

                update_transaction(
                    conn,
                    transaction_id,
                    amount=amount,
                    date=date,
                    description=description,
                    type_=type_val,
                    category_id=category_id
                )

            except Exception as e:
                print(f"Error updating transaction: {e}")




        elif choice == "4":
            try:
                transaction_id = int(input("Enter transaction ID to delete: "))
                confirm = input(f"Are you sure you want to delete transaction {transaction_id}? (y/n): ").lower()
                if confirm == "y":
                    delete_transaction(conn, transaction_id)
                    print("Transaction deleted.")
                else:
                    print("Delete cancelled.")
            except Exception as e:
                print(f"Error deleting transaction: {e}")

        elif choice == "5":
            try:
                start_date = input("Enter start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter end date (YYYY-MM-DD): ").strip()
                transactions = get_transactions_by_date_range(conn, start_date, end_date)
                if transactions:
                    print(f"\n{'ID':<5} {'Amount':<10} {'Date':<12} {'Category':<15} {'Description':<20} {'Type':<10}")
                    print("-" * 75)
                    for t in transactions:
                        print(f"{t[0]:<5} {t[1]:<10.2f} {t[2]:<12} {t[3]:<15} {t[4]:<20} {t[5]:<10}")
                else:
                    print("No transactions found in this date range.")
            except Exception as e:
                print(f"Error fetching transactions: {e}")

        elif choice == "6":
            try:
                totals = get_total_expense_by_category(conn)
                if totals:
                    print("\nTotal expense by category:")
                    for category, total in totals:
                        print(f"{category:<15}: {total:.2f}")
                else:
                    print("No expense data available.")
            except Exception as e:
                print(f"Error fetching expense totals: {e}")

        elif choice == "7":
            confirm = input("Are you sure you want to DELETE ALL transactions? This action cannot be undone. (y/n): ").lower()
            if confirm == "y":
                try:
                    delete_all_transactions(conn)
                    print("All transactions deleted.")
                except Exception as e:
                    print(f"Error deleting all transactions: {e}")
            else:
                print("Delete all cancelled.")

        elif choice == "0":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
