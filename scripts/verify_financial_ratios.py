import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

print("=" * 50)
print("FINANCIAL RATIOS TABLE")
print("=" * 50)

rows = pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM financial_ratios",
    conn,
)

print(rows)

print("\nSample Records\n")

sample = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    LIMIT 10
    """,
    conn,
)

print(sample)

conn.close()