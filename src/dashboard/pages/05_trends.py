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

st.title("📈 Trend Analysis")

ratios = run_query("""
SELECT *
FROM financial_ratios
ORDER BY year
""")

companies = sorted(
    ratios["company_id"].unique()
)

company = st.sidebar.selectbox(
    "Select Company",
    companies
)

metrics = st.multiselect(
    "Select Metrics",
    [
        "return_on_equity_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "free_cash_flow_cr",
        "debt_to_equity"
    ],
    default=["return_on_equity_pct"]
)

data = ratios[
    ratios["company_id"] == company
]

if len(metrics) == 0:

    st.warning("Select at least one metric.")

else:

    for metric in metrics:

        fig = px.line(
            data,
            x="year",
            y=metric,
            markers=True,
            title=metric
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )