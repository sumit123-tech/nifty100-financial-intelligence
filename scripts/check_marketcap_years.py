import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT
company_id,
year,
pe_ratio,
pb_ratio,
dividend_yield_pct
FROM market_cap
LIMIT 20
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()