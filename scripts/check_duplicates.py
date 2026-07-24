import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT
    company_id,
    year,
    COUNT(*) AS total
FROM financial_ratios
GROUP BY company_id, year
HAVING COUNT(*) > 1
ORDER BY company_id, year;
"""

df = pd.read_sql(query, conn)

print(df)

print("\nTotal Duplicate Records :", len(df))

conn.close()