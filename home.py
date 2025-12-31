import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import display_sidebar_info, get_df


def pct(n, total):
    return (n / total * 100) if total else 0


def render():
    display_sidebar_info()
    df = get_df()

    if df is None or len(df) == 0:
        st.error("No data available.")
        return

    st.title("🎓 UMK Insomnia & Educational Outcomes Dashboard")
    st.markdown("### Live survey dashboard (auto-updates from Google Sheets)")
    st.markdown("---")

    total = len(df)

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Responses", f"{total:,}")
    with c2:
        st.metric("Avg Sleep (est.)", f"{df['SleepHours_est'].mean():.2f} h" if "SleepHours_est" in df else "N/A")
    with c3:
        high_isi = (df["InsomniaSeverity_index"] >= 15).sum() if "InsomniaSeverity_index" in df else 0
        st.metric("High Insomnia Risk", f"{high_isi}", f"{pct(high_isi,total):.1f}%")
    with c4:
        high_stress = df["StressLevel"].astype(str).str.contains("High|Extremely", na=False).sum() if "StressLevel" in df else 0
        st.metric("High Stress", f"{high_stress}", f"{pct(high_stress,total):.1f}%")

    st.markdown("---")

    # Overview visuals (not part of member grading)
    col1, col2 = st.columns(2)

    with col1:
        if "InsomniaSeverity_index" in df:
            fig = px.histogram(df, x="InsomniaSeverity_index", nbins=10, title="Insomnia Severity Index Distribution")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if "Faculty" in df.columns:
            faculty_counts = df["Faculty"].value_counts().head(10).reset_index()
            faculty_counts.columns = ["Faculty", "Count"]
            fig = px.bar(faculty_counts, x="Count", y="Faculty", orientation="h", title="Top Faculties (Top 10)")
            st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 View raw data", expanded=False):
        st.dataframe(df, use_container_width=True, hide_index=True)


render()
