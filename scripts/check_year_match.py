import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

print("Financial Ratios Years")

print(pd.read_sql(
"""
SELECT DISTINCT year
FROM financial_ratios
ORDER BY year
LIMIT 15
""",
conn
))

print()

print("Market Cap Years")

print(pd.read_sql(
"""
SELECT DISTINCT year
FROM market_cap
ORDER BY year
LIMIT 15
""",
conn
))

conn.close()