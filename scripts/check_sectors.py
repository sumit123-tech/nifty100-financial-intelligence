import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

print("=== sectors Schema ===\n")

print(
    pd.read_sql(
        "PRAGMA table_info(sectors)",
        conn
    )
)

print("\n=== Sample Data ===\n")

print(
    pd.read_sql(
        """
        SELECT *
        FROM sectors
        LIMIT 20
        """,
        conn
    )
)

conn.close()