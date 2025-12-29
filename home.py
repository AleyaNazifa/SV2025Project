import streamlit as st

def render(df):
    st.subheader("Home")
    st.write("Dataset overview and quick summary.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Responses", f"{len(df)}")
    c2.metric("Columns", f"{df.shape[1]}")
    c3.metric("Has Insomnia Index", "Yes" if "InsomniaSeverity_index" in df.columns else "No")

    st.markdown("---")
    st.dataframe(df.head(30), use_container_width=True)
