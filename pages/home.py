import streamlit as st
from data_loader import get_dataframe_from_session

st.title("Home")
st.caption("Overview of dataset and key metrics.")

df = get_dataframe_from_session()
if df is None:
    st.warning("No data loaded yet. Go back to the main page (app) and load data.")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Responses", f"{len(df)}")

if "InsomniaSeverity_index" in df.columns:
    c2.metric("Mean Insomnia Severity", f"{df['InsomniaSeverity_index'].mean():.2f}")
else:
    c2.metric("Mean Insomnia Severity", "N/A")

if "AcademicImpact_index" in df.columns:
    c3.metric("Mean Academic Impact", f"{df['AcademicImpact_index'].mean():.2f}")
else:
    c3.metric("Mean Academic Impact", "N/A")

st.subheader("Preview")
st.dataframe(df.head(30), use_container_width=True)
