import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

print("TABLES:")
print(pd.read_sql_query(
    "SELECT name FROM sqlite_master WHERE type='table'",
    conn
))

conn.close()