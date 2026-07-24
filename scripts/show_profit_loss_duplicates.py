import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT *
FROM profitandloss
WHERE company_id = 'ADANIPORTS'
AND year = 'Mar 2013'
"""

df = pd.read_sql(query, conn)

conn.close()

print(df)
print("\nTotal Rows :", len(df))