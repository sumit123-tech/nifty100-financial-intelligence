import os
import streamlit as st

st.title("📄 Reports")

REPORT_FOLDER = "reports"

if not os.path.exists(REPORT_FOLDER):
    st.error("Reports folder not found.")
    st.stop()

files = []

for root, dirs, filenames in os.walk(REPORT_FOLDER):
    for file in filenames:
        files.append(os.path.join(root, file))

if len(files) == 0:
    st.warning("No reports available.")
    st.stop()

st.success(f"{len(files)} report files found.")

for file in sorted(files):

    filename = os.path.basename(file)

    ext = filename.split(".")[-1].upper()

    with open(file, "rb") as f:

        st.download_button(
            label=f"📥 {filename} ({ext})",
            data=f,
            file_name=filename
        )