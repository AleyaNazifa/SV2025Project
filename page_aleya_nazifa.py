import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from data_loader import display_sidebar_info, get_df

pio.templates.default = "plotly_white"

ACCENT = "#4F46E5"   # Indigo
TEXT = "#1F2937"     # Gray-800
GRID = "rgba(148,163,184,0.25)"  # Slate-300 w/ alpha


def pct(n, total):
    return (n / total * 100) if total else 0


def style(fig, title, xlab=None, ylab=None):
    fig.update_layout(
        title=title,
        font=dict(color=TEXT),
        title_font=dict(size=22, color=TEXT),
        margin=dict(l=10, r=10, t=55, b=10),
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False),
        legend=dict(title="", orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    if xlab:
        fig.update_xaxes(title_text=xlab)
    if ylab:
        fig.update_yaxes(title_text=ylab)
    return fig


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
    fig = px.histogram(
        df,
        x="SleepHours_est",
        nbins=8,
        color_discrete_sequence=[ACCENT],
    )
    fig = style(fig, "Sleep Duration (Estimated Hours)", "Hours of Sleep", "Number of Students")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A1. Histogram of estimated sleep duration (hours).")

    short = (df["SleepHours_est"] < 6).sum()
    st.markdown(
        f"**Interpretation (A1).** The distribution suggests that **{short} students ({pct(short,total):.1f}%)** "
        "sleep fewer than 6 hours per night, indicating meaningful sleep restriction. This level of reduced sleep "
        "is commonly associated with daytime fatigue and cognitive impairment, which can hinder attention and learning."
    )

    # =========================
    # A2 Box plot — SleepHours_est by Gender
    # =========================
    fig = px.box(
        df,
        x="Gender",
        y="SleepHours_est",
        points="outliers",
        color_discrete_sequence=[ACCENT],
    )
    fig = style(fig, "Sleep Duration by Gender", "Gender", "Estimated Sleep Hours")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A2. Box plot comparing estimated sleep duration by gender.")

    st.markdown(
        "**Interpretation (A2).** The box plot highlights both central tendency and variability in sleep duration "
        "across genders. Any separation in medians or differences in spread may reflect differences in routines, "
        "stress exposure, or academic workload, while outliers can signal students at higher sleep-health risk."
    )

    # =========================
    # A3 Donut — BedTime
    # =========================
    fig = px.pie(
        df,
        names="BedTime",
        hole=0.45,
        color_discrete_sequence=["#64748B", ACCENT, "#A78BFA", "#EF4444", "#94A3B8"],
    )
    fig = style(fig, "Weekday Bedtime Distribution")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A3. Donut chart of weekday bedtime categories.")

    late = df["BedTime"].astype(str).str.contains("After 12 AM", na=False).sum()
    st.markdown(
        f"**Interpretation (A3).** A total of **{late} students ({pct(late,total):.1f}%)** report sleeping after midnight. "
        "Late bedtimes can compress sleep duration when wake times are fixed for classes, and may disrupt circadian rhythm. "
        "This pattern is consistent with increased insomnia symptoms and poorer perceived sleep quality."
    )

    # =========================
    # A4 Violin — SleepQuality by BedTime
    # =========================
    fig = px.violin(
        df,
        x="BedTime",
        y="SleepQuality",
        box=True,
        points=False,
        color_discrete_sequence=[ACCENT],
    )
    fig = style(fig, "Sleep Quality by Bedtime", "Bedtime Category", "Sleep Quality (1=Poor, 5=Excellent)")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A4. Violin plot of sleep quality across bedtime groups.")

    st.markdown(
        "**Interpretation (A4).** The violin plot shows how sleep quality ratings are distributed across bedtime groups. "
        "Wider spreads and lower concentrations among later bedtime categories suggest that delayed sleep timing may be "
        "associated with poorer sleep quality and less consistent rest, supporting sleep hygiene recommendations."
    )

    # =========================
    # A5 Heatmap — DifficultyFallingAsleep vs NightWakeups
    # =========================
    heat = pd.crosstab(df["DifficultyFallingAsleep"], df["NightWakeups"])
    fig = px.imshow(
        heat,
        text_auto=True,
        color_continuous_scale=["#EEF2FF", ACCENT],
    )
    fig = style(fig, "Difficulty Falling Asleep vs Night Wakeups")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure A5. Heatmap showing co-occurrence of insomnia symptoms.")

    st.markdown(
        "**Interpretation (A5).** The heatmap indicates clustering in higher-frequency categories, implying that many "
        "students experience both difficulty initiating sleep and fragmented sleep. Co-occurring symptoms generally point "
        "to more persistent insomnia risk than isolated disturbances, strengthening the case for targeted interventions."
    )


render()
