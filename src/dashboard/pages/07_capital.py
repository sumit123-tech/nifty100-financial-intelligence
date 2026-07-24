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

st.title("💰 Capital Allocation Map")

# -----------------------------
# Load CSV
# -----------------------------

CSV_PATH = "output/capital_allocation.csv"

if not os.path.exists(CSV_PATH):
    st.error("❌ output/capital_allocation.csv not found.")
    st.stop()

data = pd.read_csv(CSV_PATH)

st.success("Capital Allocation data loaded successfully.")

# -----------------------------
# Metrics
# -----------------------------

col1, col2 = st.columns(2)

col1.metric(
    "Total Companies",
    data["company_id"].nunique()
)

col2.metric(
    "Total Records",
    len(data)
)

# -----------------------------
# Distribution
# -----------------------------

distribution = (
    data.groupby("pattern_label")
    .size()
    .reset_index(name="Companies")
)

st.subheader("Capital Allocation Distribution")

fig = px.bar(
    distribution,
    x="pattern_label",
    y="Companies",
    color="Companies",
    text="Companies",
    title="Capital Allocation Patterns"
)

fig.update_layout(
    xaxis_title="Pattern",
    yaxis_title="Companies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Treemap
# -----------------------------

st.subheader("Capital Allocation Treemap")

treemap = px.treemap(
    data,
    path=["pattern_label", "company_id"],
    title="Companies grouped by Capital Allocation Pattern"
)

st.plotly_chart(
    treemap,
    use_container_width=True
)

# -----------------------------
# Pattern Filter
# -----------------------------

st.subheader("Filter by Pattern")

selected_pattern = st.selectbox(
    "Choose Pattern",
    sorted(data["pattern_label"].unique())
)

filtered = data[
    data["pattern_label"] == selected_pattern
]

st.metric(
    "Companies in Pattern",
    filtered["company_id"].nunique()
)

st.dataframe(
    filtered,
    use_container_width=True
)

# -----------------------------
# Download CSV
# -----------------------------

csv = filtered.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered CSV",
    data=csv,
    file_name="capital_allocation_filtered.csv",
    mime="text/csv"
)

# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "NIFTY100 Financial Intelligence Dashboard | Capital Allocation Analysis"
)