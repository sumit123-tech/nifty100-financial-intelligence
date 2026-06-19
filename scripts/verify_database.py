"""
Verify SQLite Database Tables
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow"
]

for table in tables:
    count = pd.read_sql(f"SELECT COUNT(*) AS total_rows FROM {table}", conn)
    print(f"{table}: {count['total_rows'][0]} rows")

conn.close()

print("Database verification completed")