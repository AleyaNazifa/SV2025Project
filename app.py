import streamlit as st
from data_loader import load_data_ui, get_df

st.set_page_config(page_title="UMK Insomnia Dashboard", layout="wide")

st.title("UMK Insomnia & Educational Outcomes Dashboard")
st.caption("Load data here, then open pages using the sidebar.")

# Load data once
load_data_ui()

df = get_df()
if df is None:
    st.stop()

st.sidebar.header("Menu")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Aleya Aelyana", "Aleya Nazifa", "Nash"],
)

if page == "Home":
    import home
    home.render()
elif page == "Aleya Aelyana":
    import page_aleya_aelyana
    page_aleya_aelyana.render()
elif page == "Aleya Nazifa":
    import page_aleya_nazifa
    page_aleya_nazifa.render()
else:
    import page_nash
    page_nash.render()
