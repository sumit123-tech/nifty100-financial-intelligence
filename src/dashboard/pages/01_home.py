import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../..")
    )
)

import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_sectors
)

st.title("🏠 Dashboard")

companies = get_companies()
ratios = get_ratios()
sector_df = get_sectors()

st.sidebar.header("Filters")

year = st.sidebar.selectbox(
    "Financial Year",
    sorted(
        ratios["year"].unique(),
        reverse=True
    )
)

latest = ratios[
    ratios["year"] == year
]

# ================= KPI ================= #

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Companies",
    len(companies)
)

c2.metric(
    "Average ROE",
    round(
        latest["return_on_equity_pct"].mean(),
        2
    )
)

c3.metric(
    "Median P/E",
    round(
        latest["pe_ratio"].median(),
        2
    )
)

c4.metric(
    "Debt Free Companies",
    len(
        latest[
            latest["debt_to_equity"] == 0
        ]
    )
)

c5.metric(
    "Median Revenue CAGR",
    round(
        latest["revenue_cagr_5yr"].median(),
        2
    )
)

# ================= Sector Chart ================= #

fig = px.pie(
    sector_df,
    values="companies",
    names="broad_sector",
    hole=0.5,
    title="Sector Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("🏆 Top 5 Companies by Quality Score")

top5 = (
    latest[
        [
            "company_id",
            "composite_quality_score",
            "return_on_equity_pct",
            "pe_ratio"
        ]
    ]
    .sort_values(
        "composite_quality_score",
        ascending=False
    )
    .head(5)
)

st.dataframe(
    top5,
    use_container_width=True
)