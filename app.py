# app.py
import streamlit as st

st.set_page_config(page_title="E-Waste & Repair Hub", page_icon="♻️", layout="wide")

st.title("♻️ E-Waste & Device Repair Hub")
st.write(
    "Fix it, sell it, or dispose of it responsibly. "
    "Use the pages in the sidebar to get started."
)

col1, col2, col3 = st.columns(3)
col1.subheader("🔧 Repair Guides")
col1.write("Search step-by-step troubleshooting guides for common devices.")

col2.subheader("🛒 Community Board")
col2.write("Buy or sell old electronics with other students.")

col3.subheader("♻️ Disposal")
col3.write("Find out whether a device should be repaired, resold, or recycled.")