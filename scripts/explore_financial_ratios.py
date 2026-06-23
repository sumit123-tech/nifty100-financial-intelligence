"""
Explore Financial Ratios Table
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios LIMIT 5",
    conn
)

print("\nColumns:\n")
print(df.columns.tolist())

print("\nSample Data:\n")
print(df)

conn.close()