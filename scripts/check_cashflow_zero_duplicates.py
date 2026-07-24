import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT *
FROM cashflow
WHERE company_id='ABB'
ORDER BY year, record_id
"""

df = pd.read_sql(query, conn)

conn.close()

pd.set_option("display.max_columns", None)

for year in df["year"].unique():

    temp = df[df["year"] == year]

    if len(temp) > 1:
        print("\n", year)
        print(
            temp[
                [
                    "record_id",
                    "operating_activity",
                    "investing_activity",
                    "financing_activity",
                    "net_cash_flow",
                ]
            ]
        )