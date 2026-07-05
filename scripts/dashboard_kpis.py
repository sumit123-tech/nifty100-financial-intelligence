"""
Dashboard KPI Summary
Creates key metrics for dashboard visualization.
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

# Total Companies
companies = pd.read_sql(
    "SELECT COUNT(DISTINCT company_id) AS total FROM companies",
    conn
)["total"][0]

# Average ROE
avg_roe = pd.read_sql(
    """
    SELECT ROUND(AVG(return_on_equity_pct),2) AS avg_roe
    FROM financial_ratios
    WHERE return_on_equity_pct BETWEEN 0 AND 100
    """,
    conn
)["avg_roe"][0]

# Average Debt to Equity
avg_de = pd.read_sql(
    """
    SELECT ROUND(AVG(debt_to_equity),2) AS avg_de
    FROM financial_ratios
    WHERE debt_to_equity>=0
    """,
    conn
)["avg_de"][0]

# Average Sales
avg_sales = pd.read_sql(
    """
    SELECT ROUND(AVG(sales),2) AS avg_sales
    FROM profitandloss
    """,
    conn
)["avg_sales"][0]

# Average Net Profit
avg_profit = pd.read_sql(
    """
    SELECT ROUND(AVG(net_profit),2) AS avg_profit
    FROM profitandloss
    """,
    conn
)["avg_profit"][0]

summary = pd.DataFrame({
    "Metric":[
        "Total Companies",
        "Average ROE",
        "Average Debt to Equity",
        "Average Sales (Cr)",
        "Average Net Profit (Cr)"
    ],
    "Value":[
        companies,
        avg_roe,
        avg_de,
        avg_sales,
        avg_profit
    ]
})

print(summary)

summary.to_csv(
    "reports/kpi_summary.csv",
    index=False
)

conn.close()

print("\nKPI Summary Saved Successfully")