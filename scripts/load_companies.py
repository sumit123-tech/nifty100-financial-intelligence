"""
Load Companies Dataset

Reads companies.xlsx, fixes header row, cleans company_id,
and loads data into SQLite companies table.
"""

import pandas as pd
import sqlite3
from pathlib import Path

RAW_FILE = Path("data/raw/companies.xlsx")
DB_FILE = Path("database/nifty100.db")

# Read Excel with actual header row
df = pd.read_excel(RAW_FILE, header=1)

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Rename primary key column
df = df.rename(columns={"id": "company_id"})

# Clean company_id
df["company_id"] = df["company_id"].astype(str).str.strip().str.upper()

print("Companies Data Loaded")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())

# Load into SQLite
conn = sqlite3.connect(DB_FILE)

df.to_sql(
    "companies",
    conn,
    if_exists="replace",
    index=False
)

# Verify row count
count = pd.read_sql("SELECT COUNT(*) AS total_rows FROM companies", conn)

print("\nCompanies table loaded successfully")
print(count)

conn.close()