import pandas as pd
import sqlite3

df = pd.read_excel("data/raw/peer_groups.xlsx")

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

conn = sqlite3.connect("database/nifty100.db")

df.to_sql(
    "peer_groups",
    conn,
    if_exists="replace",
    index=False
)

print(pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM peer_groups",
    conn
))

conn.close()

print("Peer Groups Loaded Successfully")