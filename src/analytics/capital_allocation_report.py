import pandas as pd
import os

OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- Load ---------------- #

df = pd.read_csv("output/capital_allocation.csv")

# ---------------- Latest Pattern ---------------- #

latest = (
    df.sort_values("year")
      .groupby("company_id")
      .tail(1)
      .reset_index(drop=True)
)

# ---------------- Distribution ---------------- #

distribution = (
    latest.groupby("pattern_label")
          .size()
          .reset_index(name="companies")
          .sort_values(
              "companies",
              ascending=False
          )
)

distribution.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "capital_allocation_distribution.csv"
    ),
    index=False
)

# ---------------- Pattern Changes ---------------- #

changes = []

for company in df["company_id"].unique():

    temp = (
        df[df["company_id"] == company]
        .sort_values("year")
    )

    first_pattern = temp.iloc[0]["pattern_label"]

    last_pattern = temp.iloc[-1]["pattern_label"]

    if first_pattern != last_pattern:

        changes.append({

            "company_id": company,

            "from_pattern": first_pattern,

            "to_pattern": last_pattern

        })

changes = pd.DataFrame(changes)

changes.to_csv(

    os.path.join(

        OUTPUT_DIR,

        "pattern_changes.csv"

    ),

    index=False

)

# ---------------- Summary ---------------- #

summary = latest[
    [
        "company_id",
        "year",
        "pattern_label"
    ]
]

summary.to_csv(

    os.path.join(

        OUTPUT_DIR,

        "capital_allocation_summary.csv"

    ),

    index=False

)

# ---------------- Console ---------------- #

print("=" * 60)

print("Capital Allocation Report")

print("=" * 60)

print()

print("Companies :", len(summary))

print("Pattern Types :", distribution["pattern_label"].nunique())

print("Companies Changed Pattern :", len(changes))

print()

print("Distribution")

print(distribution)

print()

print("Generated Files")

print("✔ output/capital_allocation_distribution.csv")

print("✔ output/pattern_changes.csv")

print("✔ output/capital_allocation_summary.csv")