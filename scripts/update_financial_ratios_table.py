import sqlite3

conn = sqlite3.connect("database/nifty100.db")
cursor = conn.cursor()

new_columns = [

    "revenue_cagr_5yr REAL",

    "pat_cagr_5yr REAL",

    "eps_cagr_5yr REAL",

    "composite_quality_score REAL"

]

cursor.execute("PRAGMA table_info(financial_ratios)")

existing = [row[1] for row in cursor.fetchall()]

for column in new_columns:

    column_name = column.split()[0]

    if column_name not in existing:

        cursor.execute(

            f"ALTER TABLE financial_ratios ADD COLUMN {column}"

        )

        print(f"Added {column_name}")

    else:

        print(f"{column_name} already exists")

conn.commit()

conn.close()

print("\nfinancial_ratios table updated successfully.")