"""
Top Revenue Companies Analysis
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT
    company_id,
    ROUND(AVG(sales), 2) AS avg_sales_cr
FROM profitandloss
GROUP BY company_id
HAVING avg_sales_cr IS NOT NULL
ORDER BY avg_sales_cr DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)

print("\nTop 10 Companies by Average Revenue\n")
print(df)

df.to_csv("reports/top_revenue_companies.csv", index=False)

conn.close()

print("\nTop Revenue Report Saved")