import streamlit as st
from data_loader import get_df

def render():
    st.subheader("Aleya Aelyana — Page")
    df = get_df()
    if df is None:
        st.stop()
    st.write("Put 5 visualizations here.")
    st.dataframe(df.head(10), use_container_width=True)

