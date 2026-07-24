import sqlite3
import pandas as pd
import re
import os

DB_PATH = "database/nifty100.db"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- Database ---------------- #

conn = sqlite3.connect(DB_PATH)

analysis = pd.read_sql(
    "SELECT * FROM analysis",
    conn
)

conn.close()

# ---------------- Regex ---------------- #

pattern = re.compile(
    r"(\d+)\s*Years?:?\s*([\d.]+)%"
)

target_columns = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

records = []
failures = []

# ---------------- Parsing ---------------- #

for _, row in analysis.iterrows():

    company = row["company_id"]

    for column in target_columns:

        value = str(row[column])

        matches = pattern.findall(value)

        if matches:

            for years, pct in matches:

                records.append(
                    {
                        "company_id": company,
                        "metric_type": column,
                        "period_years": int(years),
                        "value_pct": float(pct)
                    }
                )

        else:

            failures.append(
                {
                    "company_id": company,
                    "metric_type": column,
                    "original_text": value
                }
            )

# ---------------- DataFrames ---------------- #

parsed_df = pd.DataFrame(records)

failure_df = pd.DataFrame(failures)

# ---------------- Save Files ---------------- #

parsed_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "analysis_parsed.csv"
    ),
    index=False
)

failure_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "parse_failures.csv"
    ),
    index=False
)

# ---------------- Summary ---------------- #

print("=" * 50)

print("NLP PARSER SUMMARY")

print("=" * 50)

print()

print(f"Total Parsed Records : {len(parsed_df)}")

print(f"Total Failed Records : {len(failure_df)}")

print()

print("First 5 Parsed Rows:")

print(parsed_df.head())

print()

print("Files Generated:")

print("✔ output/analysis_parsed.csv")

print("✔ output/parse_failures.csv")

print()

print("Day 29 Parser Completed Successfully.")