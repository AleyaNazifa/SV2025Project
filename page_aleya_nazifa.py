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

    # =========================
    # B1 Bar — GPA distribution
    # =========================
    fig = px.bar(
        df["GPA"].value_counts().sort_index(),
        title="GPA Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B1. Distribution of GPA among students.")

    st.markdown(
        """
**Interpretation (B1).** GPA distribution provides an overview of academic achievement.
Comparing GPA with sleep indicators helps assess whether strong academic
performance coexists with sleep deprivation.
"""
    )

    # =========================
    # B2 Stacked bar — Assignment impact by year
    # =========================
    fig = px.histogram(
        df,
        x="YearOfStudy",
        color="AssignmentImpact",
        barmode="stack",
        title="Assignment Impact by Year of Study"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B2. Stacked bar chart of assignment impact by year of study.")

    st.markdown(
        """
**Interpretation (B2).** Higher years of study tend to report greater assignment impact,
likely reflecting increased workload and time pressure that may worsen
sleep deprivation.
"""
    )

    # =========================
    # B3 Scatter — ISI vs sleep hours
    # =========================
    fig = px.scatter(
        df,
        x="SleepHours_est",
        y="InsomniaSeverity_index",
        color="GPA",
        title="Insomnia Severity vs Sleep Duration"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B3. Scatter plot of insomnia severity versus sleep duration.")

    st.markdown(
        """
**Interpretation (B3).** A negative relationship is observed: students with shorter
sleep duration generally exhibit higher insomnia severity scores.
This highlights the academic risk associated with chronic sleep loss.
"""
    )

    # =========================
    # B4 Treemap — Academic performance
    # =========================
    fig = px.treemap(
        df,
        path=["AcademicPerformance"],
        title="Composition of Academic Performance Ratings"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B4. Treemap of self-rated academic performance.")

    st.markdown(
        """
**Interpretation (B4).** The treemap shows how students perceive their academic success.
Differences between perceived and objective performance may reflect fatigue,
stress, or reduced confidence linked to poor sleep.
"""
    )

    # =========================
    # B5 Line — Responses over time
    # =========================
    df["Date"] = pd.to_datetime(df["Timestamp"]).dt.date
    fig = px.line(
        df.groupby("Date").size(),
        title="Survey Responses Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B5. Daily count of survey responses over time.")

    st.markdown(
        """
**Interpretation (B5).** The time trend confirms consistent participation,
supporting the reliability of the dataset for analysing relationships
between sleep patterns and academic outcomes.
"""
    )


render()
