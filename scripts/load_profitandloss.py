"""
Load Profit & Loss Dataset
"""

import pandas as pd
import sqlite3
from pathlib import Path

RAW_FILE = Path("data/raw/profitandloss.xlsx")
DB_FILE = Path("database/nifty100.db")

# Actual header is in row 2
df = pd.read_excel(RAW_FILE, header=1)

# Clean columns
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Rename id column
df = df.rename(columns={"id": "record_id"})

# Clean company_id
df["company_id"] = (
    df["company_id"]
    .astype(str)
    .str.strip()
    .str.upper()
)

print("Profit & Loss Dataset")
print("Shape:", df.shape)

conn = sqlite3.connect(DB_FILE)

df.to_sql(
    "profitandloss",
    conn,
    if_exists="replace",
    index=False
)

count = pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM profitandloss",
    conn
)

print(count)

conn.close()

print("Profit & Loss Loaded Successfully")