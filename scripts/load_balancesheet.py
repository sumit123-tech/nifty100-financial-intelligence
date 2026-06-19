"""
Load Balance Sheet Dataset
"""

import pandas as pd
import sqlite3
from pathlib import Path

RAW_FILE = Path("data/raw/balancesheet.xlsx")
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

print("Balance Sheet Dataset")
print("Shape:", df.shape)

conn = sqlite3.connect(DB_FILE)

df.to_sql(
    "balancesheet",
    conn,
    if_exists="replace",
    index=False
)

count = pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM balancesheet",
    conn
)

print(count)

conn.close()

print("Balance Sheet Loaded Successfully")