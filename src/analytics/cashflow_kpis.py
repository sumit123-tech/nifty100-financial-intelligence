import sqlite3
import pandas as pd
import os

DB_PATH = "database/nifty100.db"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

balance = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

# ---------------- Latest Year Data ---------------- #

cash_latest = (
    cashflow
    .sort_values(["company_id", "year"])
    .groupby("company_id")
    .tail(1)
)

balance_latest = (
    balance
    .sort_values(["company_id", "year"])
    .groupby("company_id")
    .tail(1)
)

ratio_latest = (
    ratios
    .sort_values(["company_id", "year"])
    .groupby("company_id")
    .tail(1)
)

df = (
    ratio_latest
    .merge(
        cash_latest,
        on=["company_id", "year"],
        how="left"
    )
    .merge(
        balance_latest,
        on=["company_id", "year"],
        how="left"
    )
)

records = []

distress = []

for _, row in df.iterrows():

    company = row["company_id"]

    cfo = row["cash_from_operations_cr"]

    pat = row["free_cash_flow_cr"]

    sales = row["revenue_cagr_5yr"]

    investing = row["investing_activity"]

    financing = row["financing_activity"]

    borrowings = row["borrowings"]

    # ---------- CFO Quality ----------

    if pd.notna(cfo) and pd.notna(pat) and pat != 0:

        score = round(cfo / pat, 2)

    else:

        score = None

    if score is None:

        quality = "Unknown"

    elif score > 1:

        quality = "High Quality"

    elif score >= 0.5:

        quality = "Moderate"

    else:

        quality = "Accrual Risk"

    # ---------- CapEx ----------

    if pd.notna(investing) and pd.notna(sales) and sales != 0:

        capex = abs(investing) / abs(sales) * 100

    else:

        capex = None

    if capex is None:

        cap_label = "Unknown"

    elif capex < 3:

        cap_label = "Asset Light"

    elif capex <= 8:

        cap_label = "Moderate"

    else:

        cap_label = "Capital Intensive"

    # ---------- Distress ----------

    distress_flag = False

    if (
        pd.notna(cfo)
        and pd.notna(financing)
        and cfo < 0
        and financing > 0
    ):

        distress_flag = True

        distress.append({

            "company_id": company,

            "cash_from_operations": cfo,

            "financing_activity": financing,

            "borrowings": borrowings

        })

    # ---------- Deleveraging ----------

    deleveraging = False

    if (
        pd.notna(financing)
        and financing < 0
    ):

        deleveraging = True

    # ---------- Allocation Label ----------

    if distress_flag:

        allocation = "Distress"

    elif deleveraging:

        allocation = "Deleveraging"

    elif quality == "High Quality":

        allocation = "Cash Generator"

    else:

        allocation = "Neutral"

    records.append({

        "company_id": company,

        "year": row["year"],

        "cfo_quality_score": score,

        "cfo_quality_label": quality,

        "capex_intensity_pct": capex,

        "capex_label": cap_label,

        "distress_flag": distress_flag,

        "deleveraging_flag": deleveraging,

        "capital_allocation_label": allocation

    })

# ---------------- Save ---------------- #

summary = pd.DataFrame(records)

alerts = pd.DataFrame(distress)

summary.to_excel(

    os.path.join(

        OUTPUT_DIR,

        "cashflow_intelligence.xlsx"

    ),

    index=False

)

alerts.to_csv(

    os.path.join(

        OUTPUT_DIR,

        "distress_alerts.csv"

    ),

    index=False

)

print("=" * 60)

print("Cash Flow Intelligence")

print("=" * 60)

print()

print("Companies :", len(summary))

print("Distress Alerts :", len(alerts))

print()

print(summary.head())

print()

print("Generated Files")

print("✔ output/cashflow_intelligence.xlsx")

print("✔ output/distress_alerts.csv")