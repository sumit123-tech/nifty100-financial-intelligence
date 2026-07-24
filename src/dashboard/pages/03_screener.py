import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../..")
    )
)

import streamlit as st
import plotly.express as px

from src.screener.engine import ScreenerEngine

st.title("🔍 AI Stock Screener")

# ---------------- Backend ---------------- #

engine = ScreenerEngine()

# ---------------- Sidebar ---------------- #

st.sidebar.header("Screener Filters")

preset = st.sidebar.selectbox(
    "Select Preset",
    [
        "Quality Compounder",
        "Value Pick",
        "Growth Accelerator",
        "Dividend Champion",
        "Debt-Free Blue Chip",
        "Turnaround Watch"
    ]
)

roe = st.sidebar.slider(
    "Minimum ROE (%)",
    min_value=0,
    max_value=50,
    value=15
)

de = st.sidebar.slider(
    "Maximum Debt / Equity",
    min_value=0.0,
    max_value=5.0,
    value=1.0,
    step=0.1
)

fcf = st.sidebar.slider(
    "Minimum Free Cash Flow (Cr)",
    min_value=-5000,
    max_value=50000,
    value=0
)

revenue = st.sidebar.slider(
    "Minimum Revenue CAGR (%)",
    min_value=-20,
    max_value=50,
    value=10
)

# ---------------- Data ---------------- #

result = engine.top_n(
    n=100,
    preset=preset
)

result = result[
    (result["return_on_equity_pct"] >= roe)
    &
    (result["debt_to_equity"] <= de)
    &
    (result["free_cash_flow_cr"] >= fcf)
    &
    (result["revenue_cagr_5yr"] >= revenue)
]

# ---------------- Summary ---------------- #

st.subheader("Matching Companies")

st.metric(
    "Companies Found",
    len(result)
)

c1, c2, c3 = st.columns(3)

if len(result) > 0:

    c1.metric(
        "Average Score",
        round(result["stock_score"].mean(), 2)
    )

    c2.metric(
        "Highest Score",
        round(result["stock_score"].max(), 2)
    )

    c3.metric(
        "Average ROE",
        round(result["return_on_equity_pct"].mean(), 2)
    )

else:

    c1.metric("Average Score", "N/A")
    c2.metric("Highest Score", "N/A")
    c3.metric("Average ROE", "N/A")

# ---------------- Result Table ---------------- #

st.subheader("Screening Results")

if len(result) > 0:

    st.dataframe(
        result[
            [
                "company_id",
                "broad_sector",
                "return_on_equity_pct",
                "debt_to_equity",
                "free_cash_flow_cr",
                "revenue_cagr_5yr",
                "stock_score"
            ]
        ],
        use_container_width=True
    )

else:

    st.warning("No companies matched the selected filters.")

# ---------------- Sector Chart ---------------- #

if len(result) > 0:

    st.subheader("Sector Distribution")

    sector_df = (
        result.groupby("broad_sector")
        .size()
        .reset_index(name="Companies")
    )

    fig = px.pie(
        sector_df,
        names="broad_sector",
        values="Companies",
        hole=0.45,
        title="Companies by Sector"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------- Download ---------------- #

st.subheader("Export Results")

csv = result.to_csv(index=False)

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="screener_output.csv",
    mime="text/csv"
)

engine.close()