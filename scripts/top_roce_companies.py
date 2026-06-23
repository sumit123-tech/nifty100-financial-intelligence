"""
Top 10 Companies by ROCE
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT
    company_name,
    roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)

print("\nTop 10 Companies by ROCE\n")
print(df)

conn.close()