import os
import random
from datetime import date, timedelta

import psycopg2
from faker import Faker


fake = Faker("en_IN")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "ai_analyst"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}


def get_connection():
    if not DB_CONFIG["password"]:
        raise ValueError("DB_PASSWORD is missing from .env")

    return psycopg2.connect(**DB_CONFIG)


def generate_data():
    conn = get_connection()
    cur = conn.cursor()

    # -------------------------
    # Customers
    # -------------------------
    customers = []

    cities = [
        ("Mumbai", "Maharashtra"),
        ("Delhi", "Delhi"),
        ("Bengaluru", "Karnataka"),
        ("Hyderabad", "Telangana"),
        ("Chennai", "Tamil Nadu"),
        ("Kolkata", "West Bengal"),
        ("Pune", "Maharashtra"),
        ("Ahmedabad", "Gujarat"),
        ("Jaipur", "Rajasthan"),
        ("Bhubaneswar", "Odisha"),
    ]

    for customer_id in range(1, 5001):
        city, state = random.choice(cities)

        customers.append(
            (
                customer_id,
                fake.name(),
                city,
                state,
            )
        )

    cur.executemany(
        """
        INSERT INTO customers
        (customer_id, customer_name, city, state)
        VALUES (%s, %s, %s, %s)
        """,
        customers,
    )

    # -------------------------
    # Products
    # -------------------------
    categories = {
        "Electronics": [
            "Laptop",
            "Smartphone",
            "Tablet",
            "Monitor",
            "Keyboard",
            "Headphones",
        ],
        "Home & Kitchen": [
            "Mixer",
            "Air Fryer",
            "Coffee Maker",
            "Vacuum Cleaner",
            "Cookware Set",
        ],
        "Fashion": [
            "T-Shirt",
            "Jeans",
            "Sneakers",
            "Jacket",
            "Backpack",
        ],
        "Books": [
            "Data Science Book",
            "Business Book",
            "Fiction Book",
            "Mathematics Book",
            "Programming Book",
        ],
        "Sports": [
            "Cricket Bat",
            "Football",
            "Running Shoes",
            "Yoga Mat",
            "Dumbbells",
        ],
    }

    products = []
    product_id = 1

    for category, product_names in categories.items():
        for name in product_names:
            for _ in range(4):
                products.append(
                    (
                        product_id,
                        f"{name} {product_id}",
                        category,
                        round(random.uniform(300, 100000), 2),
                    )
                )

                product_id += 1

    cur.executemany(
        """
        INSERT INTO products
        (product_id, product_name, category, price)
        VALUES (%s, %s, %s, %s)
        """,
        products,
    )

    # -------------------------
    # Orders + Order Items
    # -------------------------
    orders = []
    order_items = []

    order_id = 1
    order_item_id = 1

    start_date = date(2024, 1, 1)
    end_date = date(2025, 12, 31)

    date_range = (end_date - start_date).days

    for _ in range(20000):

        customer_id = random.randint(1, 5000)

        order_date = start_date + timedelta(
            days=random.randint(0, date_range)
        )

        number_of_items = random.randint(1, 5)

        order_items_for_order = []
        total_amount = 0

        for _ in range(number_of_items):

            product = random.choice(products)

            product_id = product[0]
            price = float(product[3])

            quantity = random.randint(1, 3)

            revenue = round(price * quantity, 2)

            total_amount += revenue

            order_items_for_order.append(
                (
                    order_item_id,
                    order_id,
                    product_id,
                    quantity,
                    revenue,
                )
            )

            order_item_id += 1

        orders.append(
            (
                order_id,
                customer_id,
                order_date,
                round(total_amount, 2),
            )
        )

        order_items.extend(order_items_for_order)

        order_id += 1

    cur.executemany(
        """
        INSERT INTO orders
        (order_id, customer_id, order_date, total_amount)
        VALUES (%s, %s, %s, %s)
        """,
        orders,
    )

    cur.executemany(
        """
        INSERT INTO order_items
        (order_item_id, order_id, product_id, quantity, revenue)
        VALUES (%s, %s, %s, %s, %s)
        """,
        order_items,
    )

    conn.commit()

    print(f"Customers inserted: {len(customers)}")
    print(f"Products inserted: {len(products)}")
    print(f"Orders inserted: {len(orders)}")
    print(f"Order items inserted: {len(order_items)}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    generate_data()