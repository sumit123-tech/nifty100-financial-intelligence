"""
Financial Health Score Engine
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT
    company_id,

    ROUND(
        AVG(
            CASE
                WHEN return_on_equity_pct BETWEEN 0 AND 100
                THEN return_on_equity_pct
            END
        ),
        2
    ) AS avg_roe,

    ROUND(
        AVG(
            CASE
                WHEN debt_to_equity >= 0
                THEN debt_to_equity
            END
        ),
        2
    ) AS avg_de

FROM financial_ratios

GROUP BY company_id
"""

df = pd.read_sql(query, conn)

# Remove missing values
df = df.dropna()

# Financial Health Score
df["health_score"] = (
    (df["avg_roe"] * 0.7)
    +
    ((1 / (df["avg_de"] + 1)) * 30)
)

df = df.sort_values(
    by="health_score",
    ascending=False
)

print("\nTop 10 Financially Healthy Companies\n")
print(
    df[
        [
            "company_id",
            "avg_roe",
            "avg_de",
            "health_score"
        ]
    ].head(10)
)

df.to_csv(
    "reports/financial_health_score.csv",
    index=False
)

conn.close()

print("\nFinancial Health Report Saved")