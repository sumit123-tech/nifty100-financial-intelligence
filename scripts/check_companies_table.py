import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

print("=== Companies Schema ===\n")

print(
    pd.read_sql(
        "PRAGMA table_info(companies)",
        conn
    )
)

print("\n=== Sample Data ===\n")

print(
    pd.read_sql(
        """
        SELECT *
        FROM companies
        LIMIT 10
        """,
        conn
    )
)

conn.close()