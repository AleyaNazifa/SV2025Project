import streamlit as st
from data_loader import get_df

def render():
    st.subheader("Home")
    df = get_df()
    if df is None:
        st.stop()

    c1, c2 = st.columns(2)
    c1.metric("Responses", f"{len(df)}")
    c2.metric("Columns", f"{df.shape[1]}")

    st.dataframe(df.head(30), use_container_width=True)

