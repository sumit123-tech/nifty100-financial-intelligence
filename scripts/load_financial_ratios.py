"""
Load Financial Ratios Dataset
"""

import pandas as pd
import sqlite3

df = pd.read_excel("data/raw/financial_ratios.xlsx")

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

conn = sqlite3.connect("database/nifty100.db")

df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

count = pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM financial_ratios",
    conn
)

print(count)

conn.close()

print("Financial Ratios Loaded Successfully")