import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from data_loader import display_sidebar_info, get_df

pio.templates.default = "plotly_white"

ACCENT = "#64748B"   # Slate
TEXT = "#1F2937"
GRID = "rgba(148,163,184,0.25)"


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

    st.title("📚 Academic Impact Analysis (Aelyana)")
    st.markdown("### Academic Outcomes Associated With Sleep Disruption")
    st.markdown("---")

    # =========================
    # B1 Bar — GPA distribution
    # =========================
    gpa_counts = df["GPA"].value_counts().reset_index()
    gpa_counts.columns = ["GPA", "Count"]

    fig = px.bar(
        gpa_counts,
        x="GPA",
        y="Count",
        color_discrete_sequence=[ACCENT],
    )
    fig = style(fig, "GPA Distribution", "GPA Range", "Number of Students")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B1. Bar chart of GPA distribution among respondents.")

    high_gpa = df["GPA"].astype(str).str.contains("3.70|4.00", na=False).sum()
    st.markdown(
        f"**Interpretation (B1).** The GPA distribution shows academic achievement levels across respondents; "
        f"**{high_gpa} students ({pct(high_gpa,total):.1f}%)** fall into the highest band (3.70–4.00). "
        "This provides context for assessing whether strong academic outcomes coincide with sleep problems."
    )

    # =========================
    # B2 Stacked bar — Assignment impact by YearOfStudy
    # =========================
    fig = px.histogram(
        df,
        x="YearOfStudy",
        color="AssignmentImpact",
        barmode="stack",
        color_discrete_sequence=["#CBD5E1", "#94A3B8", ACCENT, "#334155"],
    )
    fig = style(fig, "Assignment Impact by Year of Study", "Year of Study", "Number of Students")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B2. Stacked bar chart showing assignment impact across year of study.")

    st.markdown(
        "**Interpretation (B2).** The stacked distribution compares perceived assignment impact across academic years. "
        "If higher-year cohorts show more ‘major impact’ responses, it suggests increasing workload and time pressure, "
        "which can contribute to late-night studying and reduced sleep duration."
    )

    # =========================
    # B3 Scatter — ISI vs SleepHours_est (color by GPA)
    # =========================
    fig = px.scatter(
        df,
        x="SleepHours_est",
        y="InsomniaSeverity_index",
        color="GPA",
        opacity=0.85,
        color_discrete_sequence=px.colors.sequential.Greys,
    )
    fig = style(fig, "Insomnia Severity vs Sleep Duration (Colored by GPA)", "Estimated Sleep Hours", "ISI Score (0–28)")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B3. Scatter plot of insomnia severity against sleep duration, colored by GPA band.")

    st.markdown(
        "**Interpretation (B3).** The scatter plot supports an expected pattern: shorter sleep aligns with higher insomnia severity. "
        "Coloring by GPA allows evaluation of whether high-performing students are also exposed to poor sleep health, "
        "highlighting the potential hidden cost of academic success."
    )

    # =========================
    # B4 Treemap — Academic performance self-rating
    # =========================
    fig = px.treemap(
        df,
        path=["AcademicPerformance"],
        color_discrete_sequence=[ACCENT],
    )
    fig = style(fig, "Self-Rated Academic Performance Composition")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B4. Treemap summarizing self-rated academic performance categories.")

    excellent = df["AcademicPerformance"].astype(str).str.contains("Excellent|Very good", na=False).sum()
    st.markdown(
        f"**Interpretation (B4).** The treemap summarizes perceived academic performance, where "
        f"**{excellent} students ({pct(excellent,total):.1f}%)** rate themselves as excellent/very good. "
        "Perceptions may be influenced by fatigue and stress, and may not always match GPA bands, "
        "which is important when interpreting self-reported academic outcomes."
    )

    # =========================
    # B5 Line — responses over time
    # =========================
    df_time = df.copy()
    df_time["Date"] = pd.to_datetime(df_time["Timestamp"], errors="coerce").dt.date
    ts = df_time.groupby("Date").size().reset_index(name="Responses")

    fig = px.line(
        ts,
        x="Date",
        y="Responses",
        markers=True,
        color_discrete_sequence=[ACCENT],
    )
    fig = style(fig, "Survey Responses Over Time", "Date", "Number of Responses")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B5. Line chart showing number of survey responses per day.")

    st.markdown(
        "**Interpretation (B5).** The response trend shows how participation accumulated across time. "
        "A consistent pattern suggests dataset stability and reduces the likelihood that findings are driven by a single-day spike. "
        "This supports the credibility of relationships observed between sleep variables and academic outcomes."
    )


render()
