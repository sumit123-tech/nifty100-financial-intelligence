import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT
    company_id,
    year,
    MIN(id) AS keep_min_id,
    MAX(id) AS keep_max_id,
    COUNT(*) AS total
FROM financial_ratios
GROUP BY company_id, year
HAVING COUNT(*) > 1
ORDER BY company_id, year
"""

df = pd.read_sql(query, conn)

print(df.head(20))
print("\nDuplicate Groups:", len(df))

conn.close()