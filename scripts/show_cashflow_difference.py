import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT *
FROM cashflow
WHERE company_id='ABB'
AND year='Mar 2014'
"""

df = pd.read_sql(query, conn)

conn.close()

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print(df)