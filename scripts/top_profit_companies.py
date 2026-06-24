"""
Top Profit Companies Analysis
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT
    company_id,
    ROUND(AVG(net_profit), 2) AS avg_net_profit_cr
FROM profitandloss
GROUP BY company_id
HAVING avg_net_profit_cr IS NOT NULL
ORDER BY avg_net_profit_cr DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)

print("\nTop 10 Companies by Average Net Profit\n")
print(df)

df.to_csv(
    "reports/top_profit_companies.csv",
    index=False
)

conn.close()

print("\nTop Profit Report Saved")