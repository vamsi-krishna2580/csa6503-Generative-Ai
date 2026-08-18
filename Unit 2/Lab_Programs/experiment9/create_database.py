import sqlite3
from pathlib import Path


DB_NAME = "retail.db"


def create_database() -> None:
    """Create the retail database and insert sample data."""

    if Path(DB_NAME).exists():
        Path(DB_NAME).unlink()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE customers (
        cust_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL,
        join_date TEXT NOT NULL,
        segment TEXT NOT NULL
    );

    CREATE TABLE products (
        prod_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        unit_price REAL NOT NULL
    );

    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        cust_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (cust_id) REFERENCES customers(cust_id)
    );

    CREATE TABLE order_items (
        order_id INTEGER NOT NULL,
        prod_id INTEGER NOT NULL,
        qty INTEGER NOT NULL,
        discount_pct REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (prod_id) REFERENCES products(prod_id)
    );
    """)

    customers = [
        (1, "Arun Traders", "Chennai", "2024-01-15", "Retail"),
        (2, "Bala Stores", "Madurai", "2024-02-10", "Retail"),
        (3, "City Mart", "Coimbatore", "2024-03-05", "Corporate"),
        (4, "Delta Retail", "Salem", "2024-04-12", "Retail"),
        (5, "Elite Shop", "Trichy", "2024-05-18", "Corporate"),
        (6, "Fresh Mart", "Chennai", "2024-06-22", "Retail"),
        (7, "Green Stores", "Erode", "2024-07-11", "Retail"),
        (8, "Happy Mart", "Vellore", "2024-08-09", "Corporate")
    ]

    products = [
        (1, "Laptop Pro", "Electronics", 60000),
        (2, "Smartphone X", "Electronics", 30000),
        (3, "Office Chair", "Furniture", 8000),
        (4, "Study Desk", "Furniture", 12000),
        (5, "Mixer Pro", "Appliances", 5000),
        (6, "Air Cooler", "Appliances", 15000)
    ]

    orders = [
        (1, 1, "2025-01-10", "COMPLETED"),
        (2, 2, "2025-01-20", "COMPLETED"),
        (3, 3, "2025-02-05", "COMPLETED"),
        (4, 4, "2025-02-18", "COMPLETED"),
        (5, 5, "2025-03-10", "COMPLETED"),
        (6, 1, "2025-03-25", "COMPLETED"),
        (7, 6, "2025-04-05", "COMPLETED"),
        (8, 2, "2025-04-22", "CANCELLED"),
        (9, 3, "2025-05-14", "COMPLETED"),
        (10, 7, "2025-05-28", "COMPLETED"),
        (11, 4, "2025-06-08", "COMPLETED"),
        (12, 8, "2025-06-21", "COMPLETED"),
        (13, 5, "2025-07-04", "COMPLETED"),
        (14, 6, "2025-07-19", "COMPLETED"),
        (15, 1, "2025-08-11", "COMPLETED"),
        (16, 2, "2025-08-26", "COMPLETED"),
        (17, 3, "2025-09-09", "COMPLETED"),
        (18, 7, "2025-09-24", "COMPLETED"),
        (19, 4, "2025-10-07", "COMPLETED"),
        (20, 8, "2025-10-18", "CANCELLED"),
        (21, 5, "2025-11-05", "COMPLETED"),
        (22, 6, "2025-11-22", "COMPLETED"),
        (23, 1, "2025-12-12", "COMPLETED"),
        (24, 2, "2025-12-27", "COMPLETED"),
        (25, 3, "2026-01-08", "COMPLETED"),
        (26, 4, "2026-01-20", "COMPLETED"),
        (27, 5, "2026-02-10", "COMPLETED"),
        (28, 6, "2026-02-18", "COMPLETED"),
        (29, 7, "2026-03-07", "COMPLETED"),
        (30, 8, "2026-03-25", "COMPLETED")
    ]

    order_items = [
        (1, 1, 2, 0), (1, 3, 1, 5),
        (2, 2, 1, 0), (2, 5, 2, 10),
        (3, 4, 2, 0), (3, 6, 1, 5),
        (4, 3, 3, 0), (4, 5, 2, 0),
        (5, 1, 1, 10), (5, 6, 1, 0),
        (6, 2, 2, 5), (6, 3, 2, 0),
        (7, 4, 1, 0), (7, 5, 3, 0),
        (8, 1, 1, 0),
        (9, 2, 1, 10), (9, 6, 1, 0),
        (10, 3, 4, 0), (10, 5, 1, 0),
        (11, 4, 2, 5), (11, 1, 1, 0),
        (12, 2, 2, 0), (12, 6, 1, 10),
        (13, 5, 5, 0), (13, 3, 1, 0),
        (14, 1, 1, 5), (14, 4, 2, 0),
        (15, 2, 2, 0), (15, 6, 2, 0),
        (16, 3, 3, 0), (16, 5, 2, 5),
        (17, 1, 1, 0), (17, 4, 1, 0),
        (18, 2, 2, 10), (18, 5, 3, 0),
        (19, 6, 2, 0), (19, 3, 2, 0),
        (20, 1, 2, 0),
        (21, 4, 2, 0), (21, 5, 4, 5),
        (22, 2, 1, 0), (22, 6, 1, 0),
        (23, 1, 1, 5), (23, 3, 2, 0),
        (24, 2, 2, 0), (24, 4, 1, 0),
        (25, 5, 4, 0), (25, 6, 1, 0),
        (26, 1, 1, 0), (26, 3, 2, 0),
        (27, 2, 1, 10), (27, 5, 3, 0),
        (28, 4, 2, 0), (28, 6, 1, 0),
        (29, 1, 1, 0), (29, 3, 1, 0),
        (30, 2, 1, 5), (30, 5, 2, 0)
    ]

    cursor.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?, ?)",
        customers
    )

    cursor.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?)",
        products
    )

    cursor.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?)",
        orders
    )

    cursor.executemany(
        "INSERT INTO order_items VALUES (?, ?, ?, ?)",
        order_items
    )

    conn.commit()
    conn.close()

    print("Database created successfully.")
    print("customers:", len(customers))
    print("products:", len(products))
    print("orders:", len(orders))
    print("order_items:", len(order_items))


if __name__ == "__main__":
    create_database()