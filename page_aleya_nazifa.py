import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

from data_loader import display_sidebar_info, get_df
from cleaning_nazifa import prepare_nazifa_data

pio.templates.default = "plotly_white"

ACCENT = "#14B8A6"  # teal
TEXT = "#0F172A"
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
    st.markdown(
        f"<div class='card'><div class='card-title'>{title}</div>",
        unsafe_allow_html=True
    )


def end_card():
    st.markdown("</div>", unsafe_allow_html=True)


def caption(text: str):
    st.markdown(f"<div class='figure-caption'>{text}</div>", unsafe_allow_html=True)


def interp(text: str):
    st.markdown(
        f"<div class='interpretation'><b>Interpretation.</b> {text}</div>",
        unsafe_allow_html=True
    )


def render():
    display_sidebar_info()

    raw = get_df()
    df = prepare_nazifa_data(raw)

    if df is None or df.empty:
        st.error("No data available.")
        return

    total = len(df)

    st.title("Sleep Patterns Analysis (Nazifa)")
    st.markdown("### Sleep Duration, Timing, Quality, and Insomnia Symptoms")
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    # =========================
    # Figure A1 — Sleep Duration Distribution
    # =========================
    card("Figure A1 — Sleep Duration (Estimated Hours)")
    fig = px.histogram(df, x="SleepHours_est", nbins=8, color_discrete_sequence=[ACCENT])
    fig = style(fig, "Sleep Duration Distribution", "Hours of Sleep (Estimated)", "Number of Students")
    st.plotly_chart(fig, use_container_width=True)
    caption("Figure A1. Histogram of estimated sleep duration (hours).")

    short = (df["SleepDurationCategory"] == "Short (<6h)").sum() if "SleepDurationCategory" in df.columns else 0
    interp(
        f"The histogram indicates that {short} students ({pct(short,total):.1f}%) are short sleepers (<6 hours). "
        "A noticeable short-sleep subgroup suggests potential sleep deprivation, which is commonly linked to reduced attention, poorer memory consolidation, and decreased learning efficiency."
    )
    end_card()

    # =========================
    # Figure A2 — Sleep Duration Categories (REPLACEMENT)
    # =========================
    card("Figure A2 — Sleep Duration Categories (Short / Adequate / Long)")
    cat_order = ["Short (<6h)", "Adequate (6–8h)", "Long (>8h)"]

    if "SleepDurationCategory" in df.columns:
        cat_counts = (
            df["SleepDurationCategory"]
            .astype(str)
            .value_counts()
            .reindex(cat_order, fill_value=0)
            .reset_index()
        )
        cat_counts.columns = ["Category", "Count"]

        fig = px.bar(
            cat_counts,
            x="Category",
            y="Count",
            text="Count",
            color_discrete_sequence=[ACCENT],
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig = style(fig, "Sleep Duration Category Distribution", "Sleep Duration Category", "Number of Students")
        st.plotly_chart(fig, use_container_width=True)

        caption("Figure A2. Distribution of respondents across sleep duration categories (short, adequate, long).")

        short_n = int(cat_counts.loc[cat_counts["Category"] == "Short (<6h)", "Count"].values[0])
        interp(
            f"The category breakdown shows the proportion of students who are short, adequate, or long sleepers. "
            f"Short sleepers account for {short_n} students ({pct(short_n,total):.1f}%), representing a subgroup that may be more vulnerable to insomnia symptoms, daytime fatigue, and reduced academic alertness."
        )
    else:
        st.warning("SleepDurationCategory is missing. Please verify Nazifa cleaning module.")
    end_card()

    # =========================
    # Figure A3 — Bedtime Distribution (Donut)
    # =========================
    card("Figure A3 — Weekday Bedtime Distribution")

    tmp = df.copy()
    if "BedTime_order" in tmp.columns:
        tmp = tmp.sort_values("BedTime_order")

    fig = px.pie(
        tmp,
        names="BedTime",
        hole=0.45,
        color_discrete_sequence=["#64748B", ACCENT, "#0EA5E9", "#F59E0B", "#EF4444"],
    )
    fig = style(fig, "Bedtime Distribution (Weekdays)")
    st.plotly_chart(fig, use_container_width=True)
    caption("Figure A3. Donut chart of reported weekday bedtime categories.")

    late = df["BedTime"].astype(str).str.contains("After 12 AM", na=False).sum() if "BedTime" in df.columns else 0
    interp(
        f"{late} students ({pct(late,total):.1f}%) report sleeping after midnight. "
        "Late bedtimes can reduce sleep opportunity when wake-up times are fixed for classes, increasing the risk of fatigue and insomnia-related complaints."
    )
    end_card()

    # =========================
    # Figure A4 — Sleep Quality by Bedtime (Violin)
    # =========================
    card("Figure A4 — Sleep Quality by Bedtime")

    fig = px.violin(
        df,
        x="BedTime",
        y="SleepQuality_num",
        box=True,
        points=False,
        color_discrete_sequence=[ACCENT],
    )
    fig = style(fig, "Sleep Quality Across Bedtime Categories", "Bedtime Category", "Sleep Quality (1=Poor, 5=Excellent)")
    st.plotly_chart(fig, use_container_width=True)
    caption("Figure A4. Violin plot showing sleep quality ratings across bedtime categories.")

    interp(
        "Sleep quality varies across bedtime groups, and later bedtime categories often show lower perceived quality and wider variability. "
        "This pattern supports sleep hygiene recommendations promoting consistent and earlier bedtimes to improve restorative sleep."
    )
    end_card()

    # =========================
    # Figure A5 — Co-occurrence Heatmap (Difficulty vs Night Wakeups)
    # =========================
    card("Figure A5 — Co-occurrence of Insomnia Symptoms")

    heat = pd.crosstab(df["DifficultyFallingAsleep"], df["NightWakeups"])
    fig = px.imshow(heat, text_auto=True, color_continuous_scale=["#ECFEFF", ACCENT])
    fig = style(fig, "Difficulty Falling Asleep vs Night Wakeups")
    st.plotly_chart(fig, use_container_width=True)
    caption("Figure A5. Heatmap showing co-occurrence between difficulty initiating sleep and night awakenings.")

    both = 0
    if "FrequentDifficultyFallingAsleep" in df.columns and "FrequentNightWakeups" in df.columns:
        both = (df["FrequentDifficultyFallingAsleep"] & df["FrequentNightWakeups"]).sum()

    interp(
        f"The heatmap indicates that insomnia symptoms frequently overlap; {both} students ({pct(both,total):.1f}%) report frequent difficulty falling asleep together with frequent night awakenings. "
        "Co-occurring symptoms often reflect more severe sleep disruption than isolated problems, suggesting a subgroup that may benefit from targeted sleep interventions."
    )
    end_card()


render()
