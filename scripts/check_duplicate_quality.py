import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT
id,
company_id,
year,
free_cash_flow_cr,
capex_cr,
cash_from_operations_cr
FROM financial_ratios
WHERE company_id='ABB'
ORDER BY year,id
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()