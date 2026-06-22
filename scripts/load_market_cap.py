import pandas as pd
import sqlite3

df = pd.read_excel("data/raw/market_cap.xlsx")

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

conn = sqlite3.connect("database/nifty100.db")

df.to_sql(
    "market_cap",
    conn,
    if_exists="replace",
    index=False
)

print(pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM market_cap",
    conn
))

conn.close()

print("Market Cap Loaded Successfully")