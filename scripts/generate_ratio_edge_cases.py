import sqlite3
import pandas as pd
import os

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT

f.company_id,
f.year,

f.return_on_equity_pct,

c.roe_percentage,
c.roce_percentage,

s.broad_sector

FROM financial_ratios f

LEFT JOIN companies c
ON f.company_id = c.company_id

LEFT JOIN sectors s
ON f.company_id = s.company_id

ORDER BY
f.company_id,
f.year
"""

df = pd.read_sql(query, conn)

conn.close()

os.makedirs("output", exist_ok=True)

log_file = open(
    "output/ratio_edge_cases.log",
    "w",
    encoding="utf-8"
)

count = 0

for _, row in df.iterrows():

    # -----------------------
    # ROE Validation
    # -----------------------

    if (
        pd.notna(row["return_on_equity_pct"])
        and
        pd.notna(row["roe_percentage"])
    ):

        diff = abs(
            row["return_on_equity_pct"]
            -
            row["roe_percentage"]
        )

        if diff > 5:

            log_file.write(
                f"{row['company_id']} | "
                f"{row['year']} | "
                f"ROE Difference = {round(diff,2)} | "
                f"Category : Version Difference\n"
            )

            count += 1

    # -----------------------
    # ROCE Validation
    # -----------------------

    if pd.notna(row["roce_percentage"]):

        if row["roce_percentage"] < 0:

            log_file.write(
                f"{row['company_id']} | "
                f"{row['year']} | "
                f"ROCE appears abnormal | "
                f"Category : Data Source Issue\n"
            )

            count += 1

    # -----------------------
    # Financial Carve-out
    # -----------------------

    if row["broad_sector"] == "Financials":

        log_file.write(
            f"{row['company_id']} | "
            f"{row['year']} | "
            f"D/E Warning Suppressed "
            f"(Financial Sector)\n"
        )

        count += 1
    

log_file.close()

print("Edge Cases Logged :", count)
print("ratio_edge_cases.log generated successfully.")