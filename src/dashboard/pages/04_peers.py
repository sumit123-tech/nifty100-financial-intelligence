import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../..")
    )
)

import streamlit as st
import pandas as pd
import plotly.express as px

from src.dashboard.utils.db import run_query

st.title("🤝 Peer Comparison")

# ---------------- Load Data ---------------- #

peers = run_query("""
SELECT *
FROM peer_groups
ORDER BY peer_group_name
""")

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

ratios = ratios.merge(
    sectors,
    on="company_id",
    how="left"
)

# ---------------- Sidebar ---------------- #

peer_groups = sorted(
    peers["peer_group_name"].dropna().unique()
)

selected_group = st.sidebar.selectbox(
    "Select Peer Group",
    peer_groups
)

group_companies = peers[
    peers["peer_group_name"] == selected_group
]["company_id"]

peer_data = ratios[
    ratios["company_id"].isin(group_companies)
]

# ---------------- Summary ---------------- #

st.subheader("Peer Group Summary")

st.metric(
    "Companies",
    len(peer_data["company_id"].unique())
)

# ---------------- Average Scores ---------------- #

avg = (
    peer_data.groupby("company_id")[
        "composite_quality_score"
    ]
    .mean()
    .reset_index()
)

fig = px.bar(
    avg,
    x="company_id",
    y="composite_quality_score",
    color="composite_quality_score",
    title="Average Quality Score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------- Table ---------------- #

st.subheader("Peer Comparison Table")

table = (
    peer_data[
        [
            "company_id",
            "year",
            "return_on_equity_pct",
            "debt_to_equity",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "stock_score"
        ]
    ]
    .sort_values(
        "stock_score",
        ascending=False
    )
)

st.dataframe(
    table,
    use_container_width=True
)