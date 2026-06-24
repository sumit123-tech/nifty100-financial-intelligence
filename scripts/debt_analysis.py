"""
Debt Analysis Report
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT
    company_id,
    ROUND(
        AVG(debt_to_equity),
        2
    ) AS avg_debt_equity

FROM financial_ratios

GROUP BY company_id

ORDER BY avg_debt_equity DESC

LIMIT 10
"""

df = pd.read_sql(query, conn)

print("\nTop 10 Highest Debt Companies\n")
print(df)

df.to_csv(
    "reports/debt_analysis.csv",
    index=False
)

conn.close()

print("\nDebt Analysis Report Saved")