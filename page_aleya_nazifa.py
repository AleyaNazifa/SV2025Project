import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from data_loader import display_sidebar_info, get_df

pio.templates.default = "plotly_white"

ACCENT = "#14B8A6"  # teal-500 (NEW for Nazifa)
TEXT = "#0F172A"    # slate-900
GRID = "rgba(148,163,184,0.25)"


def pct(n, total):
    return (n / total * 100) if total else 0


def style(fig, title, xlab=None, ylab=None):
    fig.update_layout(
        title=title,
        font=dict(color=TEXT),
        title_font=dict(size=18, color=TEXT),
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


def card(title: str):
    st.markdown(f"<div class='card'><div class='card-title'>{title}</div>", unsafe_allow_html=True)


def end_card():
    st.markdown("</div>", unsafe_allow_html=True)


def caption(text: str):
    st.markdown(f"<div class='figure-caption'>{text}</div>", unsafe_allow_html=True)


def interp(text: str):
    st.markdown(f"<div class='interpretation'><b>Interpretation.</b> {text}</div>", unsafe_allow_html=True)


def render():
    display_sidebar_info()
    df = get_df()
    if df is None or len(df) == 0:
        st.error("No data available.")
        return

    total = len(df)

    st.title("😴 Sleep Patterns Analysis (Nazifa)")
    st.markdown("### Sleep Duration, Quality, and Insomnia Symptoms")
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    # =========================
    # A1 Histogram — SleepHours_est
    # =========================
    card("Figure A1 — Sleep Duration (Estimated Hours)")
    fig = px.histogram(df, x="SleepHours_est", nbins=8, color_discrete_sequence=[ACCENT])
    fig = style(fig, "Sleep Duration Distribution", "Hours of Sleep", "Number of Students")
    st.plotly_chart(fig, use_container_width=True)
    caption("Figure A1. Histogram of estimated sleep duration (hours).")

    short = (df["SleepHours_est"] < 6).sum()
    interp(
        f"The distribution indicates that {short} students ({pct(short,total):.1f}%) sleep fewer than 6 hours per night. "
        "This level of sleep restriction is commonly linked to daytime fatigue and reduced concentration, which can affect learning and productivity."
    )
    end_card()

    # =========================
    # A2 Box — SleepHours_est by Gender
    # =========================
    card("Figure A2 — Sleep Duration by Gender")
    fig = px.box(df, x="Gender", y="SleepHours_est", points="outliers", color_discrete_sequence=[ACCENT])
    fig = style(fig, "Sleep Duration by Gender", "Gender", "Estimated Sleep Hours")
    st.plotly_chart(fig, use_container_width=True)
    caption("Figure A2. Box plot comparing estimated sleep duration by gender.")
    interp(
        "The box plot highlights differences in medians and variability between genders. "
        "Outliers represent students with extremely low sleep, suggesting potential high-risk insomnia cases that may need attention."
    )
    end_card()

    # =========================
    # A3 Donut — BedTime
    # =========================
    card("Figure A3 — Weekday Bedtime Distribution")
    fig = px.pie(
        df,
        names="BedTime",
        hole=0.45,
        color_discrete_sequence=["#64748B", ACCENT, "#0EA5E9", "#F59E0B", "#EF4444"],
    )
    fig = style(fig, "Bedtime Distribution")
    st.plotly_chart(fig, use_container_width=True)
    caption("Figure A3. Donut chart of weekday bedtime categories.")

    late = df["BedTime"].astype(str).str.contains("After 12 AM", na=False).sum()
    interp(
        f"{late} students ({pct(late,total):.1f}%) report sleeping after midnight. "
        "Late bedtimes can compress total sleep time and disrupt circadian rhythm, increasing the likelihood of poorer sleep quality and insomnia symptoms."
    )
    end_card()

    # =========================
    # A4 Violin — SleepQuality by BedTime
    # =========================
    card("Figure A4 — Sleep Quality by Bedtime")
    fig = px.violin(df, x="BedTime", y="SleepQuality", box=True, points=False, color_discrete_sequence=[ACCENT])
    fig = style(fig, "Sleep Quality Across Bedtime Groups", "Bedtime Category", "Sleep Quality (1=Poor, 5=Excellent)")
    st.plotly_chart(fig, use_container_width=True)
    caption("Figure A4. Violin plot of sleep quality across bedtime groups.")
    interp(
        "Later bedtime categories show wider distributions and lower central tendency in quality ratings, implying less consistent and less restorative sleep. "
        "This supports recommendations for consistent bedtimes as part of sleep hygiene."
    )
    end_card()

    # =========================
    # A5 Heatmap — DifficultyFallingAsleep vs NightWakeups
    # =========================
    card("Figure A5 — Co-occurrence of Insomnia Symptoms")
    heat = pd.crosstab(df["DifficultyFallingAsleep"], df["NightWakeups"])
    fig = px.imshow(heat, text_auto=True, color_continuous_scale=["#ECFEFF", ACCENT])
    fig = style(fig, "Difficulty Falling Asleep vs Night Wakeups")
    st.plotly_chart(fig, use_container_width=True)
    caption("Figure A5. Heatmap showing co-occurrence of insomnia symptoms.")
    interp(
        "Higher-frequency clusters indicate many students experience difficulty initiating sleep together with night awakenings. "
        "Co-occurring symptoms suggest more persistent insomnia risk rather than occasional sleep disturbance."
    )
    end_card()


render()
