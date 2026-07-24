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
ORDER BY company_id, year
"""

duplicates = pd.read_sql(query, conn)

print(duplicates)

print("\nTotal Duplicate Company-Year Pairs :", len(duplicates))

conn.close()