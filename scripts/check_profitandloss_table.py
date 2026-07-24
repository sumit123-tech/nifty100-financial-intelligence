import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

print("Profit & Loss Table Structure\n")

columns = pd.read_sql(
    "PRAGMA table_info(profitandloss)",
    conn
)

print(columns[["name", "type"]])

print("\nTotal Rows\n")

rows = pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM profitandloss",
    conn
)

print(rows)

print("\nSample Data\n")

sample = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        sales,
        net_profit,
        eps
    FROM profitandloss
    LIMIT 10
    """,
    conn,
)

print(sample)

conn.close()