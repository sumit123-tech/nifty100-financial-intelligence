import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

print("=== Profit & Loss ===")

print(pd.read_sql("""
SELECT company_id,year,COUNT(*) total
FROM profitandloss
GROUP BY company_id,year
HAVING COUNT(*)>1
LIMIT 20
""",conn))

print()

print("=== Balance Sheet ===")

print(pd.read_sql("""
SELECT company_id,year,COUNT(*) total
FROM balancesheet
GROUP BY company_id,year
HAVING COUNT(*)>1
LIMIT 20
""",conn))

conn.close()