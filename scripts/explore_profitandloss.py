"""
Explore Profit & Loss Table
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM profitandloss LIMIT 5",
    conn
)

print("\nColumns:\n")
print(df.columns.tolist())

print("\nSample Data:\n")
print(df)

conn.close()