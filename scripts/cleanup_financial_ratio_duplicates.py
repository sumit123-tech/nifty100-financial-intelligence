import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

# Load complete table
df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

# Columns used to determine which row is more complete
score_columns = [
    "free_cash_flow_cr",
    "capex_cr",
    "cash_from_operations_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "eps_cagr_5yr",
    "composite_quality_score"
]

rows_to_delete = []

groups = df.groupby(["company_id", "year"])

for (company, year), group in groups:

    if len(group) == 1:
        continue

    scores = []

    for _, row in group.iterrows():

        score = 0

        for col in score_columns:

            value = row[col]

            if pd.notna(value):

                if isinstance(value, (int, float)):

                    if value != 0:
                        score += 1

                else:
                    score += 1

        scores.append((row["id"], score))

    # Highest score wins
    scores.sort(key=lambda x: (-x[1], x[0]))

    keep_id = scores[0][0]

    for row_id, _ in scores[1:]:

        rows_to_delete.append(row_id)

cursor = conn.cursor()

deleted = 0

for row_id in rows_to_delete:

    cursor.execute(
        "DELETE FROM financial_ratios WHERE id=?",
        (int(row_id),)
    )

    deleted += cursor.rowcount

conn.commit()

print(f"Rows Deleted : {deleted}")

remaining = pd.read_sql(
    """
    SELECT company_id,year,COUNT(*) total
    FROM financial_ratios
    GROUP BY company_id,year
    HAVING COUNT(*)>1
    """,
    conn,
)

print("\nRemaining Duplicate Groups")

print(remaining)

conn.close()