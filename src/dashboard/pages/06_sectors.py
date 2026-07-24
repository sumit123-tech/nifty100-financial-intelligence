import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../..")
    )
)

import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import run_query

st.title("🏭 Sector Analysis")

# ---------------- Load Data ---------------- #

ratios = run_query("""
SELECT *
FROM financial_ratios
""")

sectors = run_query("""
SELECT
company_id,
broad_sector
FROM sectors
""")

data = ratios.merge(
    sectors,
    on="company_id",
    how="left"
)

# ---------------- Sidebar ---------------- #

sector_list = sorted(
    data["broad_sector"].dropna().unique()
)

selected_sector = st.sidebar.selectbox(
    "Select Sector",
    sector_list
)

sector_data = data[
    data["broad_sector"] == selected_sector
].copy()

# ---------------- Bubble Size ---------------- #

sector_data["bubble_size"] = (
    sector_data["free_cash_flow_cr"]
    .fillna(0)
    .abs()
)

# যদি সব value 0 হয় তাহলে minimum size দাও
sector_data.loc[
    sector_data["bubble_size"] == 0,
    "bubble_size"
] = 1

# ---------------- Summary ---------------- #

st.metric(
    "Companies",
    sector_data["company_id"].nunique()
)

# ---------------- Bubble Chart ---------------- #

fig = px.scatter(
    sector_data,
    x="revenue_cagr_5yr",
    y="return_on_equity_pct",
    size="bubble_size",
    color="company_id",
    hover_name="company_id",
    size_max=40,
    title="Revenue CAGR vs ROE"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------- Average Metrics ---------------- #

st.subheader("Average Sector Metrics")

avg = (
    sector_data[
        [
            "return_on_equity_pct",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "stock_score"
        ]
    ]
    .mean()
    .reset_index()
)

avg.columns = [
    "Metric",
    "Value"
]

fig2 = px.bar(
    avg,
    x="Metric",
    y="Value",
    color="Value",
    text="Value",
    title="Average Sector Metrics"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ---------------- Raw Data ---------------- #

st.subheader("Sector Companies")

st.dataframe(
    sector_data[
        [
            "company_id",
            "year",
            "return_on_equity_pct",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "free_cash_flow_cr",
            "stock_score"
        ]
    ],
    use_container_width=True
)