import sqlite3
import pandas as pd
import os

DB_PATH = "database/nifty100.db"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- Database ---------------- #

conn = sqlite3.connect(DB_PATH)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

# ---------- Latest Record Per Company ---------- #

latest = (
    ratios
    .sort_values(["company_id", "year"])
    .groupby("company_id")
    .tail(1)
    .reset_index(drop=True)
)

records = []

# ---------------- Rules ---------------- #

for _, row in latest.iterrows():

    company = row["company_id"]

    roe = row["return_on_equity_pct"]
    debt = row["debt_to_equity"]
    rev = row["revenue_cagr_5yr"]

    # ---------- PRO 1 ----------

    if pd.notna(roe) and roe >= 20:

        records.append({
            "company_id": company,
            "type": "Pro",
            "rule_id": "PRO01",
            "text": "High ROE above 20%",
            "confidence_pct": 90
        })

    # ---------- PRO 2 ----------

    if pd.notna(debt) and debt == 0:

        records.append({
            "company_id": company,
            "type": "Pro",
            "rule_id": "PRO02",
            "text": "Debt Free Balance Sheet",
            "confidence_pct": 95
        })

    # ---------- PRO 3 ----------

    if pd.notna(rev) and rev >= 15:

        records.append({
            "company_id": company,
            "type": "Pro",
            "rule_id": "PRO03",
            "text": "Strong Revenue CAGR above 15%",
            "confidence_pct": 88
        })

    # ---------- CON 1 ----------

    if pd.notna(debt) and debt > 2:

        records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "CON01",
            "text": "High Debt Ratio",
            "confidence_pct": 84
        })

    # ---------- CON 2 ----------

    if pd.notna(roe) and roe < 10:

        records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "CON02",
            "text": "Weak Return on Equity",
            "confidence_pct": 82
        })

    # ---------- CON 3 ----------

    if pd.notna(rev) and rev < 5:

        records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "CON03",
            "text": "Low Revenue Growth",
            "confidence_pct": 80
        })

# ---------------- Output ---------------- #

output = pd.DataFrame(records)

output.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "pros_cons_generated.csv"
    ),
    index=False
)

print("=" * 60)
print("Pros & Cons Generator")
print("=" * 60)

print(f"Companies Processed : {latest['company_id'].nunique()}")
print(f"Rules Generated     : {len(output)}")

print()

print(output.head(10))

print()

print("Saved -> output/pros_cons_generated.csv")