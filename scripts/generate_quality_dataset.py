import sqlite3
import pandas as pd
import os

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("database/nifty100.db")

# -----------------------------
# Load Financial Quality Data
# -----------------------------
query = """
SELECT
    company_id,
    year,
    return_on_equity_pct,
    revenue_cagr_5yr,
    revenue_cagr_5yr_flag,
    pat_cagr_5yr,
    pat_cagr_5yr_flag,
    eps_cagr_5yr,
    eps_cagr_5yr_flag,
    composite_quality_score
FROM financial_ratios
"""

df = pd.read_sql(query, conn)

conn.close()

# -----------------------------
# Save CSV
# -----------------------------
os.makedirs("output", exist_ok=True)

df.to_csv(
    "output/financial_quality_dataset.csv",
    index=False
)

print(df.head())

print("\nfinancial_quality_dataset.csv generated successfully.")