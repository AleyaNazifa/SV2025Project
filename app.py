import streamlit as st
from data_loader import load_data_ui, get_df

import home
import page_aleya_aelyana
import page_aleya_nazifa
import page_nash

st.set_page_config(page_title="UMK Insomnia Dashboard", layout="wide")

st.title("UMK Insomnia & Educational Outcomes Dashboard")
st.caption("Load data once, then explore pages from the sidebar.")

# Load data
load_data_ui()
df = get_df()
if df is None:
    st.stop()

# Menu
st.sidebar.header("Menu")
page = st.sidebar.radio(
    "Go to",
    ["Home", "AleyaAelyana", "AleyaNazifa", "Nash"],
    index=0
)

if page == "Home":
    home.render(df)
elif page == "AleyaAelyana":
    page_aleya_aelyana.render(df)
elif page == "AleyaNazifa":
    page_aleya_nazifa.render(df)
else:
    page_nash.render(df)
