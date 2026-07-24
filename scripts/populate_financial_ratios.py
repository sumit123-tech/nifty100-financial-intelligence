import sqlite3
import pandas as pd

from cagr import calculate_cagr
from ratios import composite_quality_score

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("database/nifty100.db")

# -----------------------------
# Load Profit & Loss Data
# -----------------------------
query = """
SELECT
    p.company_id,
    p.year,
    p.sales,
    p.net_profit,
    p.eps,
    f.return_on_equity_pct
FROM profitandloss p
LEFT JOIN financial_ratios f
ON p.company_id = f.company_id
AND p.year = f.year
ORDER BY p.company_id, p.year
"""

df = pd.read_sql(query, conn)

print("Rows Loaded :", len(df))
print(df.head())

# -----------------------------
# Calculate Revenue CAGR (5 Year)
# -----------------------------

results = []

companies = df["company_id"].unique()

for company in companies:

    company_df = (
        df[df["company_id"] == company]
        .sort_values("year")
        .reset_index(drop=True)
    )

    for i in range(len(company_df)):

        revenue_cagr = None
        revenue_flag = None

        if i >= 5:

            start = company_df.loc[i - 5, "sales"]
            end = company_df.loc[i, "sales"]

            revenue_cagr, revenue_flag = calculate_cagr(
                start,
                end,
                5
            )

        # -----------------------------
        # PAT CAGR
        # -----------------------------
        pat_cagr = None
        pat_flag = None

        if i >= 5:

            start = company_df.loc[i - 5, "net_profit"]
            end = company_df.loc[i, "net_profit"]

            pat_cagr, pat_flag = calculate_cagr(
                start,
                end,
                5
            )

        # -----------------------------
        # EPS CAGR
        # -----------------------------
        eps_cagr = None
        eps_flag = None

        if i >= 5:

            start = company_df.loc[i - 5, "eps"]
            end = company_df.loc[i, "eps"]

            eps_cagr, eps_flag = calculate_cagr(
                start,
                end,
                5
            )

        quality_score = composite_quality_score(
            company_df.loc[i, "return_on_equity_pct"],
            revenue_cagr,
            pat_cagr,
            eps_cagr,
        )

        results.append({

            "company_id": company_df.loc[i, "company_id"],
            "year": company_df.loc[i, "year"],

            "revenue_cagr_5yr": revenue_cagr,
            "revenue_cagr_5yr_flag": revenue_flag,

            "pat_cagr_5yr": pat_cagr,
            "pat_cagr_5yr_flag": pat_flag,

            "eps_cagr_5yr": eps_cagr,
            "eps_cagr_5yr_flag": eps_flag,

            "composite_quality_score": quality_score

        })

result_df = pd.DataFrame(results)

print("\nRevenue CAGR Preview\n")

print(result_df.head(15))

# --------------------------------------------------
# Update financial_ratios Table
# --------------------------------------------------

cursor = conn.cursor()

updated = 0

for _, row in result_df.iterrows():

    cursor.execute(
        """
        UPDATE financial_ratios
        SET

        revenue_cagr_5yr = ?,
        revenue_cagr_5yr_flag = ?,

        pat_cagr_5yr = ?,
        pat_cagr_5yr_flag = ?,

        eps_cagr_5yr = ?,
        eps_cagr_5yr_flag = ?,

        composite_quality_score = ?

        WHERE company_id = ?
        AND year = ?
        """,
        (
            row["revenue_cagr_5yr"],
            row["revenue_cagr_5yr_flag"],

            row["pat_cagr_5yr"],
            row["pat_cagr_5yr_flag"],

            row["eps_cagr_5yr"],
            row["eps_cagr_5yr_flag"],

            row["composite_quality_score"],

            row["company_id"],
            row["year"],
        ),
    )

    updated += cursor.rowcount

conn.commit()

print(f"\nRows Updated : {updated}")


# --------------------------------------------------
# Verify Database
# --------------------------------------------------

verify = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        revenue_cagr_5yr,
        revenue_cagr_5yr_flag,
        pat_cagr_5yr,
        pat_cagr_5yr_flag,
        eps_cagr_5yr,
        eps_cagr_5yr_flag,
        composite_quality_score
    FROM financial_ratios
    LIMIT 10
    """,
    conn,
)

print("\nVerification\n")

print(verify)

conn.close()