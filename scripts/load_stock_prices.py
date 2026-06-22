"""
Load Stock Prices Dataset
"""

import pandas as pd
import sqlite3

df = pd.read_excel("data/raw/stock_prices.xlsx")

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

conn = sqlite3.connect("database/nifty100.db")

df.to_sql(
    "stock_prices",
    conn,
    if_exists="replace",
    index=False
)

print(pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM stock_prices",
    conn
))

conn.close()

print("Stock Prices Loaded Successfully")