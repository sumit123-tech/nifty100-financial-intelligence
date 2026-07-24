import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

print("=== financial_ratios schema ===")
schema = pd.read_sql(
    "PRAGMA table_info(financial_ratios);",
    conn
)
print(schema)

print("\n=== Create Table SQL ===")
sql = pd.read_sql(
    """
    SELECT sql
    FROM sqlite_master
    WHERE type='table'
      AND name='financial_ratios';
    """,
    conn
)
print(sql.iloc[0, 0])

conn.close()