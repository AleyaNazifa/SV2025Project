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

    total = len(df)

    st.title("📚 Academic Impact Analysis")
    st.markdown("### How Sleep Affects Academic Performance")
    st.markdown("---")

    # B1 Bar — GPA counts
    gpa_counts = df["GPA"].value_counts().reset_index()
    gpa_counts.columns = ["GPA", "Count"]
    fig = px.bar(gpa_counts, x="GPA", y="Count", title="GPA Distribution")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B1. Bar chart of GPA distribution.")
    st.markdown(
        "**Interpretation (B1).** GPA distribution summarises achievement levels and provides context for "
        "examining whether sleep problems are present even among higher-performing students."
    )

    # B2 Stacked bar — Assignment impact by YearOfStudy
    fig = px.histogram(
        df, x="YearOfStudy", color="AssignmentImpact",
        barmode="stack", title="Assignment Impact by Year of Study"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B2. Stacked bars comparing assignment impact across year of study.")
    st.markdown(
        "**Interpretation (B2).** If higher years show larger ‘major impact’ segments, it suggests workload "
        "escalation may amplify sleep-related academic difficulties."
    )

    # B3 Scatter — ISI vs SleepHours_est
    fig = px.scatter(
        df, x="SleepHours_est", y="InsomniaSeverity_index",
        color="GPA", title="Insomnia Severity vs Sleep Duration"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B3. Scatter plot of insomnia severity against sleep duration (colored by GPA band).")
    st.markdown(
        "**Interpretation (B3).** Students with shorter sleep frequently show higher insomnia severity, "
        "indicating sleep restriction and insomnia symptoms may coexist with academic demands."
    )

    # B4 Treemap — AcademicPerformance
    fig = px.treemap(df, path=["AcademicPerformance"], title="Self-Rated Academic Performance Composition")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B4. Treemap of self-rated academic performance.")
    st.markdown(
        "**Interpretation (B4).** The composition of self-ratings reflects perceived success; mismatch between "
        "perception and objective GPA may indicate fatigue, stress, or reduced confidence."
    )

    # B5 Line — Responses over time
    df_time = df.copy()
    df_time["Date"] = pd.to_datetime(df_time["Timestamp"], errors="coerce").dt.date
    ts = df_time.groupby("Date").size().reset_index(name="Responses")
    fig = px.line(ts, x="Date", y="Responses", markers=True, title="Survey Responses Over Time")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B5. Line chart showing number of responses per day.")
    st.markdown(
        "**Interpretation (B5).** A steady response pattern supports dataset stability and reduces the chance "
        "that results are driven by one-time anomalies."
    )


render()
