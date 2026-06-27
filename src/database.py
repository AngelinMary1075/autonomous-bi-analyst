import sqlite3
import os

# Define the database path (creates a data folder in your current directory)
DB_DIR = "./data"
DB_PATH = os.path.join(DB_DIR, "business_data.db")

def init_db():
    # 1. Ensure the directory exists
    os.makedirs(DB_DIR, exist_ok=True)
    
    # 2. Connect to SQLite (This creates the file if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"Creating database at: {DB_PATH}...")

    # 3. Create Tables
    # Sales Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            product_id TEXT,
            product_name TEXT,
            category TEXT,
            units_sold INTEGER,
            revenue REAL
        )
    ''')

    # Inventory Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            product_id TEXT PRIMARY KEY,
            product_name TEXT,
            stock_level INTEGER,
            restock_threshold INTEGER,
            unit_cost REAL
        )
    ''')

    # 4. Clear old data if running a clean wipe
    cursor.execute("DELETE FROM sales")
    cursor.execute("DELETE FROM inventory")

    # 5. Insert Rich Mock Data
    mock_sales = [
        ('2026-05-01', 'P001', 'Laptop Pro', 'Electronics', 12, 14400.00),
        ('2026-05-03', 'P002', 'Wireless Mouse', 'Electronics', 45, 1125.00),
        ('2026-05-15', 'P003', 'Ergonomic Chair', 'Furniture', 8, 2400.00),
        ('2026-06-01', 'P001', 'Laptop Pro', 'Electronics', 18, 21600.00),
        ('2026-06-10', 'P002', 'Wireless Mouse', 'Electronics', 60, 1500.00),
        ('2026-06-14', 'P004', '4K Monitor', 'Electronics', 10, 4000.00),
        ('2026-06-20', 'P003', 'Ergonomic Chair', 'Furniture', 12, 3600.00),
        ('2026-06-25', 'P005', 'Desk Lamp', 'Furniture', 25, 625.00),
    ]

    mock_inventory = [
        ('P001', 'Laptop Pro', 15, 5, 800.00),
        ('P002', 'Wireless Mouse', 120, 20, 12.00),
        ('P003', 'Ergonomic Chair', 4, 5, 180.00), # Low Stock!
        ('P004', '4K Monitor', 22, 8, 250.00),
        ('P005', 'Desk Lamp', 45, 10, 15.00),
    ]

    cursor.executemany(
        "INSERT INTO sales (date, product_id, product_name, category, units_sold, revenue) VALUES (?, ?, ?, ?, ?, ?)", 
        mock_sales
    )
    
    cursor.executemany(
        "INSERT INTO inventory (product_id, product_name, stock_level, restock_threshold, unit_cost) VALUES (?, ?, ?, ?, ?)", 
        mock_inventory
    )

    # 6. Commit changes and close
    conn.commit()
    conn.close()
    print("Database successfully generated with Sales and Inventory records!")

if __name__ == "__main__":
    create_mock_database()