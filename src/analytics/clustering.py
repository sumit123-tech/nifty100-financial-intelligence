import os
import sqlite3

import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

DB_PATH = "database/nifty100.db"

OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql("""

SELECT
company_id,
return_on_equity_pct,
operating_profit_margin_pct,
debt_to_equity,
revenue_cagr_5yr,
pat_cagr_5yr,
free_cash_flow_cr

FROM financial_ratios

WHERE year='Mar 2024'

""", conn)

conn.close()

features = [
    "return_on_equity_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "free_cash_flow_cr"
]

df[features] = df[features].fillna(0)

scaler = StandardScaler()

X = scaler.fit_transform(df[features])

kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

df["cluster"] = kmeans.fit_predict(X)

label_map = {
    0: "Quality Compounder",
    1: "Growth",
    2: "Value",
    3: "Turnaround",
    4: "Dividend"
}

df["cluster_label"] = df["cluster"].map(label_map)

output = df[
    [
        "company_id",
        "cluster",
        "cluster_label"
    ]
]

output.to_csv(
    "output/cluster_labels.csv",
    index=False
)

print("="*50)
print("Cluster Analysis Completed")
print("="*50)

print(output.head())

print()

print("Companies :", len(output))

print("Saved -> output/cluster_labels.csv")