"""
retails_mysql_demo.py
Full workflow using mysql.connector and pandas.
"""

import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import os
import sys
from getpass import getpass

# ---------- USER CONFIG ----------
# Set these to your MySQL server credentials.
# You can hardcode (not recommended) or prompt for password.
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
# MYSQL_PASSWORD = "your_password"    # optionally set here
MYSQL_PASSWORD = None   # will prompt if None

# ---------- Helper functions ----------
def prompt_password_if_needed():
    global MYSQL_PASSWORD
    if not MYSQL_PASSWORD:
        MYSQL_PASSWORD = getpass("MySQL password for user '{}': ".format(MYSQL_USER))

def get_server_connection():
    """Connect to MySQL server (no DB specified)."""
    prompt_password_if_needed()
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        autocommit=True  # autocommit while creating DB
    )

def get_db_connection(db_name):
    """Connect to a specific database."""
    prompt_password_if_needed()
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=db_name,
        autocommit=False  # commit explicitly for transactional control
    )

def show_df_from_query(conn, sql, description=None):
    """Helper to run query and print a pandas DataFrame nicely."""
    if description:
        print("\n" + description)
    df = pd.read_sql_query(sql, conn)
    if df.empty:
        print("(no rows)")
    else:
        print(df.to_string(index=False))
    return df

# ---------- Main workflow ----------
def main():
    DB_NAME = "retails"

    # 1) Connect to MySQL server and create database 'retails'
    try:
        server_conn = get_server_connection()
    except mysql.connector.Error as err:
        print("ERROR: Could not connect to MySQL server:", err)
        sys.exit(1)

    cursor = server_conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` DEFAULT CHARACTER SET 'utf8mb4'")
        print(f"Step 1: Database '{DB_NAME}' created (or already exists).")
    except mysql.connector.Error as err:
        print("Failed creating database:", err)
        cursor.close()
        server_conn.close()
        sys.exit(1)
    finally:
        cursor.close()
        server_conn.close()

    # 2) Connect to DB and create tables customer and orders
    try:
        conn = get_db_connection(DB_NAME)
    except mysql.connector.Error as err:
        print("ERROR: Could not connect to database:", err)
        sys.exit(1)

    cur = conn.cursor()
    try:
        # Create customer table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS customer (
                customer_id INT PRIMARY KEY,
                age INT,
                city VARCHAR(100),
                gender VARCHAR(20)
            ) ENGINE=InnoDB;
        """)
        # Create orders table without is_sale first
        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                order_date DATE,
                amount DECIMAL(10,2),
                customer_id INT,
                FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
                    ON DELETE RESTRICT ON UPDATE CASCADE
            ) ENGINE=InnoDB;
        """)
        conn.commit()
        print("Step 2: Created tables 'customer' and 'orders'.")
    except mysql.connector.Error as err:
        print("Error creating tables:", err)
        conn.rollback()
        cur.close()
        conn.close()
        sys.exit(1)

    # 3) Add 'is_sale' column in orders (if not exists)
    try:
        # MySQL does not support IF NOT EXISTS for ADD COLUMN in older versions,
        # so we check INFORMATION_SCHEMA first.
        cur.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
            WHERE table_schema=%s AND table_name='orders' AND column_name='is_sale';
        """, (DB_NAME,))
        exists = cur.fetchone()[0]
        if not exists:
            cur.execute("ALTER TABLE orders ADD COLUMN is_sale TINYINT(1) NOT NULL DEFAULT 0;")
            conn.commit()
            print("Step 3: Added column 'is_sale' to 'orders'.")
        else:
            print("Step 3: Column 'is_sale' already exists in 'orders'.")
    except mysql.connector.Error as err:
        print("Error altering table:", err)
        conn.rollback()
        cur.close()
        conn.close()
        sys.exit(1)

    # 4) Insert values into the customer table and display the contents.
    customers = [
        (1001, 34, 'Austin', 'male'),
        (1002, 37, 'Houston', 'male'),
        (1003, 25, 'Austin', 'female'),
        (1004, 28, 'Houston', 'female'),
        (1005, 22, 'Dallas', 'male')
    ]
    try:
        # Clean slate for demo: remove existing rows with same ids to avoid duplicate PK errors
        cur.executemany("DELETE FROM customer WHERE customer_id = %s;", [(c[0],) for c in customers])
        cur.executemany("INSERT INTO customer (customer_id, age, city, gender) VALUES (%s, %s, %s, %s);", customers)
        conn.commit()
        print("\nStep 4: Inserted customers.")
    except mysql.connector.Error as err:
        print("Error inserting customers:", err)
        conn.rollback()
        cur.close()
        conn.close()
        sys.exit(1)

    show_df_from_query(conn, "SELECT * FROM customer ORDER BY customer_id;", "Step 4: Current customer table:")

    # 5) Show the details of customers who are located in Austin City.
    show_df_from_query(conn, "SELECT * FROM customer WHERE city = 'Austin';", "Step 5: Customers located in Austin:")

    # 6) Group customers based on location and display the information.
    show_df_from_query(conn, "SELECT city, COUNT(*) AS customer_count FROM customer GROUP BY city ORDER BY city;", "Step 6: Group customers by location (counts):")

    # 7) Group customers based on their gender and display the information.
    show_df_from_query(conn, "SELECT gender, COUNT(*) AS customer_count FROM customer GROUP BY gender ORDER BY gender;", "Step 7: Group customers by gender (counts):")

    # 8) Insert values into the orders table and display the contents.
    # Provided tuples used a customer index 1..5; map them to customer IDs 1001..1005.
    orders_input = [
        ('2022-10-01', 100.25, 1),
        ('2022-10-02', 200.75, 2),
        ('2022-10-03', 500.00, 3),
        ('2022-10-03', 600.00, 4),
        ('2022-10-04', 600.00, 5)
    ]
    mapped_orders = [(d, amt, 1000 + idx) for (d, amt, idx) in orders_input]
    try:
        # Remove any rows in orders that would conflict with this demo (optional)
        # Then insert mapped orders
        # We won't set order_id (AUTO_INCREMENT).
        insert_sql = "INSERT INTO orders (order_date, amount, customer_id) VALUES (%s, %s, %s);"
        cur.executemany(insert_sql, mapped_orders)
        conn.commit()
        print("\nStep 8: Inserted orders.")
    except mysql.connector.Error as err:
        print("Error inserting orders:", err)
        conn.rollback()
        cur.close()
        conn.close()
        sys.exit(1)

    show_df_from_query(conn, "SELECT * FROM orders ORDER BY order_id;", "Step 8: Current orders table:")

    # (Optional) Update is_sale: mark orders with amount >= 500 as sale (=1)
    try:
        cur.execute("UPDATE orders SET is_sale = 1 WHERE amount >= 500;")
        conn.commit()
        print("\nUpdated 'is_sale' flag for amount >= 500.")
    except mysql.connector.Error as err:
        print("Error updating is_sale:", err)
        conn.rollback()

    show_df_from_query(conn, "SELECT * FROM orders ORDER BY order_id;", "Orders after updating is_sale:")

    # 9) Show order details that were purchased on 2022-10-03.
    show_df_from_query(conn, "SELECT * FROM orders WHERE order_date = '2022-10-03' ORDER BY amount DESC;", "Step 9: Orders on 2022-10-03:")

    # 10) Show orders that have an order amount of more than 300.
    show_df_from_query(conn, "SELECT * FROM orders WHERE amount > 300 ORDER BY amount DESC;", "Step 10: Orders with amount > 300:")

    # 11) Show all orders placed on 2022-10-03 and represent it in sorted form with respect to the amount spent.
    show_df_from_query(conn, "SELECT * FROM orders WHERE order_date = '2022-10-03' ORDER BY amount DESC;", "Step 11: Orders on 2022-10-03 sorted by amount (descending):")

    # 12) Count the number of distinct days in the data.
    cur.execute("SELECT COUNT(DISTINCT order_date) FROM orders;")
    distinct_days = cur.fetchone()[0]
    print("\nStep 12: Number of distinct order dates:", distinct_days)

    # 13) Count the orders grouped by date.
    show_df_from_query(conn, "SELECT order_date, COUNT(*) AS orders_count FROM orders GROUP BY order_date ORDER BY order_date;", "Step 13: Orders count grouped by date:")

    # 14) Calculate the average order amount for all days.
    # a) overall average
    cur.execute("SELECT AVG(amount) FROM orders;")
    overall_avg = cur.fetchone()[0]
    print("\nStep 14a: Overall average order amount (all orders):", float(overall_avg) if overall_avg is not None else None)

    # b) average per day
    show_df_from_query(conn, "SELECT order_date, AVG(amount) AS avg_amount FROM orders GROUP BY order_date ORDER BY order_date;", "Step 14b: Average order amount per day:")

    # Close connection
    cur.close()
    conn.close()
    print("\nDone. Database connection closed.")

if __name__ == "__main__":
    main()