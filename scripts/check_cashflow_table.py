import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

print("Cashflow Table Columns:\n")

columns = pd.read_sql("PRAGMA table_info(cashflow)", conn)

print(columns[["name", "type"]])

print("\nSample Data:\n")

sample = pd.read_sql("SELECT * FROM cashflow LIMIT 5", conn)

print(sample)

conn.close()