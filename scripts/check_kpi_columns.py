import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

schema = pd.read_sql(
    "PRAGMA table_info(financial_ratios)",
    conn,
)

print(schema[["name"]])

conn.close()