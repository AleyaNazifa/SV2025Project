import streamlit as st
from data_loader import (
    load_from_url,
    load_from_upload,
    ensure_engineered_columns,
    set_dataframe_in_session,
)

st.set_page_config(page_title="UMK Sleep & Academic Dashboard", layout="wide")

st.title("UMK Insomnia & Educational Outcomes")
st.caption("Multi-page Streamlit application (data source + visual analysis).")

st.sidebar.header("Data Source")

mode = st.sidebar.radio("Select mode", ["Live Google Sheet (Auto)", "Upload CSV"], index=0)

refresh = st.sidebar.button("Refresh data now")

if refresh:
    st.cache_data.clear()
    st.rerun()

if mode == "Live Google Sheet (Auto)":
    st.sidebar.write("https://docs.google.com/spreadsheets/d/e/2PACX-1vSf4umx6QNDel99If8P2otizAHj7jEDxFIsqandbD0zYVzfDheZo2YVkK1_zknpDKjHnBuYWCINgcCe/pub?output=csv")
    csv_url = st.sidebar.text_input("Google Sheet CSV URL", value="")

    if not csv_url.strip():
        st.info("Enter your Google Sheet CSV URL in the sidebar.")
        st.stop()

    df = load_from_url(csv_url.strip())

else:
    uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if uploaded is None:
        st.info("Upload a CSV file to begin.")
        st.stop()

    df = load_from_upload(uploaded)

df = ensure_engineered_columns(df)
set_dataframe_in_session(df)

st.success(f"Data loaded successfully. Rows: {len(df)}, Columns: {df.shape[1]}")

st.write("Use the page navigation on the left sidebar to view different visualizations.")
st.write("Recommended pages:")
st.markdown("- **Home** (overview & dataset summary)\n- **Insomnia Visualisation** (the 5 required plots)\n- **Subgroup Comparison** (faculty/year comparisons for creativity)")
