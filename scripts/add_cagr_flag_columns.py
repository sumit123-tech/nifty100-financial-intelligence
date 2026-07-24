import sqlite3

conn = sqlite3.connect("database/nifty100.db")
cursor = conn.cursor()

columns = [
    "revenue_cagr_5yr_flag TEXT",
    "pat_cagr_5yr_flag TEXT",
    "eps_cagr_5yr_flag TEXT"
]

cursor.execute("PRAGMA table_info(financial_ratios)")
existing = [row[1] for row in cursor.fetchall()]

for column in columns:
    name = column.split()[0]

    if name not in existing:
        cursor.execute(f"ALTER TABLE financial_ratios ADD COLUMN {column}")
        print(f"Added {name}")
    else:
        print(f"{name} already exists")

conn.commit()
conn.close()

print("\nCAGR flag columns added successfully.")