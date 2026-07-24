import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT *
FROM cashflow
ORDER BY company_id, year
"""

df = pd.read_sql(query, conn)

conn.close()

duplicates = (
    df.groupby(["company_id", "year"])
      .size()
      .reset_index(name="total")
)

duplicates = duplicates[duplicates["total"] > 1]

print("Duplicate Groups:", len(duplicates))

same = 0
different = 0

for _, row in duplicates.iterrows():

    company = row["company_id"]
    year = row["year"]

    temp = (
        df[
            (df.company_id == company) &
            (df.year == year)
        ]
        .drop(columns=["record_id"])
    )

    if temp.drop_duplicates().shape[0] == 1:
        same += 1
    else:
        different += 1
        print(company, year, "DIFFERENT")

print("\nIdentical Duplicate Groups :", same)
print("Different Duplicate Groups :", different)