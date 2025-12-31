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

    st.title("😴 Sleep Patterns Analysis (Nazifa)")
    st.markdown("### Sleep Duration, Quality, and Insomnia Symptoms")
    st.markdown("---")

    # =========================
    # A1 Histogram — SleepHours_est
    # =========================
    fig = px.histogram(df, x="SleepHours_est", nbins=8, title="Sleep Duration (Estimated Hours)")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A1. Histogram of estimated sleep duration (hours).")

    short = (df["SleepHours_est"] < 6).sum()
    st.markdown(
        f"""
**Interpretation (A1).** The histogram indicates that **{short} students ({pct(short,total):.1f}%)** sleep under 6 hours per night.
This suggests meaningful sleep restriction that can impair attention, memory consolidation, and overall daytime functioning.
"""
    )

    # =========================
    # A2 Box plot — SleepHours_est by Gender
    # =========================
    fig = px.box(df, x="Gender", y="SleepHours_est", title="Sleep Duration by Gender")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A2. Box plot comparing estimated sleep duration by gender.")

    st.markdown(
        """
**Interpretation (A2).** Differences in median and spread may reflect different routines, academic workload, or stress exposure.
Outliers also highlight students experiencing extremely short sleep, which may indicate higher insomnia risk.
"""
    )

    # =========================
    # A3 Donut — BedTime
    # =========================
    fig = px.pie(df, names="BedTime", hole=0.45, title="Weekday Bedtime Distribution")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A3. Donut chart of weekday bedtime categories.")

    late = df["BedTime"].astype(str).str.contains("After 12 AM", na=False).sum()
    st.markdown(
        f"""
**Interpretation (A3).** **{late} students ({pct(late,total):.1f}%)** report going to bed after midnight.
Late bedtimes can reduce total sleep duration (especially with fixed class times) and may worsen sleep quality and insomnia symptoms.
"""
    )

    # =========================
    # A4 Violin — SleepQuality by BedTime
    # =========================
    fig = px.violin(df, x="BedTime", y="SleepQuality", box=True, title="Sleep Quality by Bedtime")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A4. Violin plot of sleep quality across bedtime groups.")

    st.markdown(
        """
**Interpretation (A4).** Wider distributions and lower central tendency among later bedtime groups suggest that delayed sleep timing
may be associated with poorer perceived sleep quality. This supports the idea that sleep hygiene and circadian timing matter.
"""
    )

    # =========================
    # A5 Heatmap — DifficultyFallingAsleep vs NightWakeups
    # =========================
    heat = pd.crosstab(df["DifficultyFallingAsleep"], df["NightWakeups"])
    fig = px.imshow(heat, text_auto=True, title="Difficulty Falling Asleep vs Night Wakeups")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A5. Heatmap showing co-occurrence of insomnia symptoms.")

    st.markdown(
        """
**Interpretation (A5).** Concentration of counts in higher-frequency categories indicates that many students experience
multiple insomnia symptoms simultaneously (difficulty initiating sleep plus fragmented sleep), rather than isolated sleep issues.
"""
    )


render()
