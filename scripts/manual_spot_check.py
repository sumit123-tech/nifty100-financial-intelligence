import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

companies = [
    "ABB",
    "ASIANPAINT",
    "TCS"
]

for company in companies:

    print("\n" + "=" * 60)
    print(company)
    print("=" * 60)

    query = f"""
    SELECT

        f.company_id,
        f.year,

        f.return_on_equity_pct,
        f.revenue_cagr_5yr,

        p.sales,
        p.net_profit,

        b.equity_capital,
        b.reserves

    FROM financial_ratios f

    LEFT JOIN profitandloss p
        ON f.company_id=p.company_id
        AND f.year=p.year

    LEFT JOIN balancesheet b
        ON f.company_id=b.company_id
        AND f.year=b.year

    WHERE f.company_id='{company}'

    ORDER BY f.year
    """

    df = pd.read_sql(query, conn)

    print(df.tail(8))

conn.close()