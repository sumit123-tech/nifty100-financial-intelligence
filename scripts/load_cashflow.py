"""
Load Cash Flow Dataset
"""

import pandas as pd
import sqlite3
from pathlib import Path

RAW_FILE = Path("data/raw/cashflow.xlsx")
DB_FILE = Path("database/nifty100.db")

df = pd.read_excel(RAW_FILE, header=1)

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

df = df.rename(columns={"id": "record_id"})

df["company_id"] = (
    df["company_id"]
    .astype(str)
    .str.strip()
    .str.upper()
)

print("Cash Flow Dataset")
print("Shape:", df.shape)

conn = sqlite3.connect(DB_FILE)

df.to_sql(
    "cashflow",
    conn,
    if_exists="replace",
    index=False
)

count = pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM cashflow",
    conn
)

print(count)

conn.close()

print("Cash Flow Loaded Successfully")