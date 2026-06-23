"""
Top 10 Companies by Clean Average ROE

This script filters unrealistic ROE outliers and ranks companies
based on average Return on Equity.
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT
    company_id,
    ROUND(AVG(return_on_equity_pct), 2) AS avg_roe
FROM financial_ratios
WHERE return_on_equity_pct BETWEEN 0 AND 100
GROUP BY company_id
HAVING avg_roe IS NOT NULL
ORDER BY avg_roe DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)

print("\nTop 10 Companies by Clean Average ROE\n")
print(df)

df.to_csv("reports/top_roe_companies.csv", index=False)

conn.close()

print("\nROE ranking report saved successfully")