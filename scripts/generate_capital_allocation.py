import sqlite3
import pandas as pd
import os

from ratios import capital_allocation_pattern

# -----------------------------
# Database Connection
# -----------------------------
DB_PATH = "database/nifty100.db"

conn = sqlite3.connect(DB_PATH)

# -----------------------------
# Load Cash Flow Table
# -----------------------------
query = """
SELECT
    company_id,
    year,
    operating_activity,
    investing_activity,
    financing_activity
FROM cashflow
"""

df = pd.read_sql(query, conn)

conn.close()

# -----------------------------
# Generate Signs
# -----------------------------
df["cfo_sign"] = df["operating_activity"].apply(
    lambda x: "+" if x >= 0 else "-"
)

df["cfi_sign"] = df["investing_activity"].apply(
    lambda x: "+" if x >= 0 else "-"
)

df["cff_sign"] = df["financing_activity"].apply(
    lambda x: "+" if x >= 0 else "-"
)

# -----------------------------
# Pattern Classification
# -----------------------------
df["pattern_label"] = df.apply(
    lambda row: capital_allocation_pattern(
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"],
    ),
    axis=1,
)

# -----------------------------
# Keep Required Columns
# -----------------------------
result = df[
    [
        "company_id",
        "year",
        "cfo_sign",
        "cfi_sign",
        "cff_sign",
        "pattern_label",
    ]
]

# -----------------------------
# Save CSV
# -----------------------------
os.makedirs("output", exist_ok=True)

result.to_csv(
    "output/capital_allocation.csv",
    index=False,
)

print(result.head())

print("\ncapital_allocation.csv generated successfully.")