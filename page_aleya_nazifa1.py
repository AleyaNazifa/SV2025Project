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

    st.title("😴 Sleep Patterns Analysis")
    st.markdown("### Sleep Duration, Quality, and Insomnia Symptoms")
    st.markdown("---")

    # A1 Histogram — SleepHours_est
    fig = px.histogram(df, x="SleepHours_est", nbins=8, title="Sleep Duration (Estimated Hours)")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A1. Histogram of estimated sleep duration (hours).")
    short = (df["SleepHours_est"] < 6).sum()
    st.markdown(
        f"**Interpretation (A1).** **{short} students ({pct(short,total):.1f}%)** sleep under 6 hours, "
        "indicating meaningful sleep restriction that can impair attention and memory."
    )

    # A2 Box — SleepHours_est by Gender
    fig = px.box(df, x="Gender", y="SleepHours_est", title="Sleep Duration by Gender")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A2. Box plot comparing estimated sleep duration by gender.")
    st.markdown(
        "**Interpretation (A2).** Differences in median and spread may reflect differing routines, workload, "
        "and stress exposure between genders, which can shape sleep duration."
    )

    # A3 Donut — BedTime
    fig = px.pie(df, names="BedTime", hole=0.45, title="Weekday Bedtime Distribution")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A3. Donut chart of weekday bedtime categories.")
    late = df["BedTime"].astype(str).str.contains("After 12 AM", na=False).sum()
    st.markdown(
        f"**Interpretation (A3).** **{late} students ({pct(late,total):.1f}%)** go to bed after midnight, "
        "which can reduce total sleep time and worsen insomnia symptoms when wake times are fixed."
    )

    # A4 Violin — SleepQuality by BedTime
    fig = px.violin(df, x="BedTime", y="SleepQuality", box=True, title="Sleep Quality by Bedtime")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A4. Violin plot of sleep quality across bedtime groups.")
    st.markdown(
        "**Interpretation (A4).** Wider distributions and lower central tendency for later bedtimes suggest "
        "delayed sleep timing may be associated with poorer perceived sleep quality."
    )

    # A5 Heatmap — DifficultyFallingAsleep vs NightWakeups
    heat = pd.crosstab(df["DifficultyFallingAsleep"], df["NightWakeups"])
    fig = px.imshow(heat, text_auto=True, title="Difficulty Falling Asleep vs Night Wakeups")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A5. Heatmap showing co-occurrence of insomnia symptoms.")
    st.markdown(
        "**Interpretation (A5).** Clusters at higher-frequency categories indicate many students experience "
        "multiple insomnia symptoms simultaneously, not just isolated sleep issues."
    )


render()
