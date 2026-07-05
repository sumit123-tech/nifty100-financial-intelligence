import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

# Show columns
columns = pd.read_sql("PRAGMA table_info(financial_ratios);", conn)

print("\nFinancial Ratios Table Structure\n")
print(columns[["name", "type"]])

print("\nTotal Rows\n")
print(pd.read_sql("SELECT COUNT(*) AS total_rows FROM financial_ratios;", conn))

conn.close()