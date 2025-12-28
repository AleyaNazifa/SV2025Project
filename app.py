import streamlit as st
from data_loader import (
    load_from_url,
    load_from_upload,
    ensure_engineered_columns,
    set_dataframe_in_session,
)

st.set_page_config(page_title="UMK Insomnia Dashboard", layout="wide")

st.title("UMK Insomnia & Educational Outcomes Dashboard")
st.caption("Load data here. Then open each member page from the sidebar.")

st.sidebar.header("Data Source")
mode = st.sidebar.radio("Select mode", ["Live Google Sheet (Auto)", "Upload CSV"], index=0)

if st.sidebar.button("Refresh data now"):
    st.cache_data.clear()
    st.rerun()

if mode == "Live Google Sheet (Auto)":
    csv_url = st.sidebar.text_input("Published Google Sheet CSV URL", value="")
    if not csv_url.strip():
        st.info("Paste your published Google Sheet CSV URL to load live data.")
        st.stop()
    df = load_from_url(csv_url.strip())
else:
    uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if uploaded is None:
        st.info("Upload your CSV to begin.")
        st.stop()
    df = load_from_upload(uploaded)

df = ensure_engineered_columns(df)
set_dataframe_in_session(df)

st.success(f"Data loaded successfully. Rows: {len(df)} | Columns: {df.shape[1]}")

st.markdown("### Pages")
st.markdown(
    "- **1) Sleep & Insomnia Overview** (AleyaAelyana)\n"
    "- **2) Academic Impact & Performance** (AleyaNazifa)\n"
    "- **3) Lifestyle, Stress & Factors** (Nash)\n"
)
st.write("Use the left sidebar to open the pages.")
