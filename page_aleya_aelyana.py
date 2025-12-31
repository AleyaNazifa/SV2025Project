import streamlit as st
import pandas as pd
import numpy as np
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

    st.title("😴 Sleep Patterns Analysis")
    st.markdown("### Sleep Duration, Quality, and Insomnia Symptoms")
    st.markdown("---")

    # =========================
    # A1 Histogram — Sleep hours
    # =========================
    df["SleepHours_num"] = (
        df["SleepHours"]
        .astype(str)
        .str.extract(r"(\d+)")
        .astype(float)
    )

    fig = px.histogram(
        df,
        x="SleepHours_num",
        nbins=6,
        title="Sleep Duration Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A1. Histogram showing distribution of sleep duration (hours).")

    short = (df["SleepHours_num"] < 6).sum()
    st.markdown(
        f"""
**Interpretation (A1).** The histogram shows that **{short} students ({pct(short,total):.1f}%)**
sleep less than 6 hours per night, indicating widespread sleep deprivation.
Insufficient sleep duration is a known risk factor for impaired concentration,
fatigue, and academic underperformance.
"""
    )

    # =========================
    # A2 Box plot — Sleep hours by gender
    # =========================
    fig = px.box(
        df,
        x="Gender",
        y="SleepHours_num",
        title="Sleep Duration by Gender"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A2. Box plot comparing sleep duration by gender.")

    st.markdown(
        """
**Interpretation (A2).** The box plot highlights variability in sleep duration between genders.
Differences in median and spread may reflect lifestyle, academic workload,
or stress-related factors influencing sleep behaviour.
"""
    )

    # =========================
    # A3 Donut — Bedtime
    # =========================
    fig = px.pie(
        df,
        names="BedTime",
        hole=0.45,
        title="Typical Bedtime Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A3. Donut chart of weekday bedtime distribution.")

    late = df["BedTime"].str.contains("After 12 AM", na=False).sum()
    st.markdown(
        f"""
**Interpretation (A3).** A total of **{late} students ({pct(late,total):.1f}%)**
report sleeping after midnight. Late bedtimes can disrupt circadian rhythm,
reduce total sleep time, and contribute to insomnia symptoms.
"""
    )

    # =========================
    # A4 Violin — Sleep quality vs bedtime
    # =========================
    fig = px.violin(
        df,
        x="BedTime",
        y="SleepQuality",
        box=True,
        title="Sleep Quality by Bedtime"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A4. Violin plot of sleep quality across bedtime categories.")

    st.markdown(
        """
**Interpretation (A4).** Students who sleep later tend to report lower sleep quality,
with wider variability. This suggests that delayed bedtimes may negatively
affect perceived restfulness and sleep satisfaction.
"""
    )

    # =========================
    # A5 Heatmap — Insomnia symptoms
    # =========================
    heat = pd.crosstab(
        df["DifficultyFallingAsleep"],
        df["NightWakeups"]
    )

    fig = px.imshow(
        heat,
        text_auto=True,
        title="Difficulty Falling Asleep vs Night Wakeups"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A5. Heatmap showing relationship between insomnia symptoms.")

    st.markdown(
        """
**Interpretation (A5).** The heatmap shows clustering of students who experience both
difficulty initiating sleep and frequent night awakenings, indicating
co-occurring insomnia symptoms rather than isolated sleep disturbances.
"""
    )


render()
