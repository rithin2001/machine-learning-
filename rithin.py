import sqlite3
import random
from faker import Faker
from datetime import datetime
import os

fake = Faker('en_IN')

# Define product catalog
products = [
    {"product_id": "PROD001", "name": "Wireless Earbuds", "category": "Electronics", "price": 1499},
    {"product_id": "PROD002", "name": "Yoga Mat", "category": "Fitness", "price": 899},
    {"product_id": "PROD003", "name": "Smartwatch", "category": "Wearables", "price": 3499},
    {"product_id": "PROD004", "name": "Bluetooth Speaker", "category": "Audio", "price": 1999},
    {"product_id": "PROD005", "name": "Laptop Stand", "category": "Accessories", "price": 1299}
]

payment_methods = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery"]
order_statuses = ["Delivered", "Shipped", "Cancelled", "Returned"]

# Create SQLite database and table
def setup_database(db_name="ecom_data.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT,
            order_date TEXT,
            product_id TEXT,
            product_name TEXT,
            category TEXT,
            quantity INTEGER,
            price_per_unit REAL,
            total_amount REAL,
            payment_method TEXT,
            order_status TEXT,
            shipping_address TEXT,
            device TEXT,
            browser TEXT
        )
    """)
    conn.commit()
    return conn

# Generate and insert synthetic data
def generate_and_insert_data(conn, num_records=1000):
    cursor = conn.cursor()
    for i in range(num_records):
        product = random.choice(products)
        quantity = random.randint(1, 5)
        total = product["price"] * quantity
        order_date = fake.date_between(start_date='-1y', end_date='today').strftime("%Y-%m-%d")
        cursor.execute("""
            INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"ORD{i+1000}",
            f"CUST{random.randint(100,999)}",
            order_date,
            product["product_id"],
            product["name"],
            product["category"],
            quantity,
            product["price"],
            total,
            random.choice(payment_methods),
            random.choice(order_statuses),
            fake.address().replace("\n", ", "),
            random.choice(["Android Mobile", "iPhone", "Windows Laptop", "MacBook"]),
            random.choice(["Chrome", "Safari", "Edge", "Firefox"])
        ))
    conn.commit()

# Run everything
if __name__ == "__main__":
    conn = setup_database()
    generate_and_insert_data(conn)
    conn.close()
    print("Synthetic ECOM data inserted into database successfully.")




SELECT 
    o.order_id,
    o.order_date,
    o.product_id,
    o.total_amount,
    c.name AS customer_name,
    c.email
FROM 
    orders o
JOIN 
    customers c ON o.customer_id = c.customer_id;

SELECT * FROM orders_2024
UNION ALL
SELECT * FROM orders_2025;
