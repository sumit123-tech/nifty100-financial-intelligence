"""
Dashboard Summary Dataset

Creates a master dataset for dashboard visualization
by combining company, sector, financial ratio,
market cap, and financial health score outputs.
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT
    c.company_id,
    c.company_name,
    s.broad_sector,
    s.sub_sector,
    s.market_cap_category,
    c.roce_percentage,
    c.roe_percentage,
    r.return_on_equity_pct,
    r.debt_to_equity,
    r.net_profit_margin_pct,
    r.operating_profit_margin_pct,
    r.free_cash_flow_cr,
    m.market_cap_crore,
    m.pe_ratio,
    m.pb_ratio,
    m.ev_ebitda,
    m.dividend_yield_pct
FROM companies c
LEFT JOIN sectors s
    ON c.company_id = s.company_id
LEFT JOIN financial_ratios r
    ON c.company_id = r.company_id
LEFT JOIN market_cap m
    ON c.company_id = m.company_id
"""

df = pd.read_sql(query, conn)

# Clean unrealistic ROE values
df["clean_roe_pct"] = df["return_on_equity_pct"].where(
    df["return_on_equity_pct"].between(0, 100)
)

# Company level aggregation
summary = (
    df.groupby(
        [
            "company_id",
            "company_name",
            "broad_sector",
            "sub_sector",
            "market_cap_category"
        ],
        as_index=False
    )
    .agg({
        "clean_roe_pct": "mean",
        "debt_to_equity": "mean",
        "net_profit_margin_pct": "mean",
        "operating_profit_margin_pct": "mean",
        "free_cash_flow_cr": "mean",
        "market_cap_crore": "mean",
        "pe_ratio": "mean",
        "pb_ratio": "mean",
        "ev_ebitda": "mean",
        "dividend_yield_pct": "mean",
        "roce_percentage": "mean"
    })
)

summary = summary.round(2)

summary.to_csv(
    "reports/dashboard_summary.csv",
    index=False
)

print("Dashboard Summary Created Successfully")
print(summary.head())

conn.close()