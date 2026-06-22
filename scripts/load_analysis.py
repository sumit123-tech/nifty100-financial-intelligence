import pandas as pd
import sqlite3

df = pd.read_excel(
    "data/raw/analysis.xlsx",
    header=1
)

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

conn = sqlite3.connect("database/nifty100.db")

df.to_sql(
    "analysis",
    conn,
    if_exists="replace",
    index=False
)

print(pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM analysis",
    conn
))

conn.close()

print("Analysis Loaded Successfully")