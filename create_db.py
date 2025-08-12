"""
Run this script to generate the sample SQLite database at `data/sample.db`.
It creates three tables: sales, customers, feedback.

Usage:
    python create_db.py
"""
import os
import sqlite3
import pandas as pd

DATA_DIR = "data"
DB_PATH = os.path.join(DATA_DIR, "sample.db")

SALES_CSV = """
order_id,order_date,customer_id,product,category,quantity,price,region
1,2024-01-05,101,AlphaPhone,Electronics,2,299.99,North
2,2024-01-07,102,BetaPad,Electronics,1,499.00,South
3,2024-01-12,103,CypherWatch,Accessories,3,79.99,West
4,2024-02-02,101,AlphaPhone,Electronics,1,299.99,North
5,2024-02-14,104,DeltaEar,Accessories,2,49.50,East
6,2024-03-03,105,GammaCharger,Accessories,5,19.99,South
7,2024-03-15,106,BetaPad,Electronics,1,499.00,West
8,2024-04-01,107,AlphaPhone,Electronics,3,299.99,East
9,2024-04-07,102,CypherWatch,Accessories,1,79.99,North
10,2024-04-20,108,EchoCase,Accessories,4,9.99,South
"""

CUSTOMERS_CSV = """
customer_id,name,signup_date,segment,country
101,Acme Corp,2023-10-01,Enterprise,IN
102,Better Foods,2023-11-12,SMB,IN
103,Charlie Retail,2023-12-05,SMB,US
104,Delta Clinics,2024-01-22,Enterprise,US
105,Eco Supplies,2024-02-04,SMB,IN
106,FreshMart,2024-03-10,SMB,IN
107,GreenTech,2024-03-28,Enterprise,US
108,HomeSpark,2024-04-12,Consumer,IN
"""

FEEDBACK_CSV = """
feedback_id,customer_id,order_id,rating,comments,created_at
1,101,1,5,"Great product and fast delivery",2024-01-06
2,102,2,4,"Satisfied but packaging can improve",2024-01-08
3,103,3,2,"Product stopped working within a week",2024-01-15
4,101,4,5,"Repeat purchase due to excellent support",2024-02-03
5,104,5,4,"Good quality, will reorder",2024-02-16
6,105,6,3,"Charger incompatible with our devices",2024-03-05
7,106,7,4,"Arrived on time",2024-03-16
8,107,8,5,"Outstanding experience",2024-04-02
9,102,9,3,"Average build quality",2024-04-08
10,108,10,4,"Value for money",2024-04-21
"""


def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def write_csvs():
    open(os.path.join(DATA_DIR, "sales.csv"), "w").write(SALES_CSV.strip())
    open(os.path.join(DATA_DIR, "customers.csv"), "w").write(CUSTOMERS_CSV.strip())
    open(os.path.join(DATA_DIR, "feedback.csv"), "w").write(FEEDBACK_CSV.strip())


def create_sqlite_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        sales = pd.read_csv(os.path.join(DATA_DIR, "sales.csv"), parse_dates=["order_date"])
        customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"), parse_dates=["signup_date"])
        feedback = pd.read_csv(os.path.join(DATA_DIR, "feedback.csv"), parse_dates=["created_at"])

        sales.to_sql("sales", conn, if_exists="replace", index=False)
        customers.to_sql("customers", conn, if_exists="replace", index=False)
        feedback.to_sql("feedback", conn, if_exists="replace", index=False)

        print(f"Created database at {DB_PATH} with tables: sales, customers, feedback")
    finally:
        conn.close()


if __name__ == "__main__":
    ensure_data_dir()
    write_csvs()
    create_sqlite_db()
