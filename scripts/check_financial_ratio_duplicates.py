import sqlite3
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT *
FROM financial_ratios
WHERE company_id='ABB'
AND year='Mar 2014'
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()