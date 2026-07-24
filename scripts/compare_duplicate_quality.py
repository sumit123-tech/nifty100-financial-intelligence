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
    cash_from_operations_cr,

    revenue_cagr_5yr,
    pat_cagr_5yr,
    eps_cagr_5yr,

    composite_quality_score

FROM financial_ratios

WHERE company_id='ADANIPORTS'
AND year='Mar 2013'

ORDER BY id
"""

df = pd.read_sql(query, conn)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print(df)

conn.close()