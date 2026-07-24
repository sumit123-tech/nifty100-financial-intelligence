import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

print(pd.read_sql("PRAGMA table_info(market_cap)", conn)[["name"]])

conn.close()