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

    st.title("📚 Academic Impact Analysis (Aelyana)")
    st.markdown("### How Sleep Affects Academic Performance")
    st.markdown("---")

    # =========================
    # B1 Bar — GPA distribution
    # =========================
    gpa_counts = df["GPA"].value_counts().reset_index()
    gpa_counts.columns = ["GPA", "Count"]

    fig = px.bar(gpa_counts, x="GPA", y="Count", title="GPA Distribution")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B1. Bar chart of GPA distribution among respondents.")

    high_gpa = df["GPA"].astype(str).str.contains("3.70|4.00", na=False).sum()
    st.markdown(
        f"""
**Interpretation (B1).** The GPA distribution provides context for academic outcomes. In this dataset, **{high_gpa} students ({pct(high_gpa,total):.1f}%)**
are in the highest GPA band (3.70–4.00). This enables comparison of high achievement against sleep disruption indicators.
"""
    )

    st.markdown("---")

    # =========================
    # B2 Stacked bar — Assignment impact by YearOfStudy
    # =========================
    fig = px.histogram(
        df,
        x="YearOfStudy",
        color="AssignmentImpact",
        barmode="stack",
        title="Assignment Impact by Year of Study",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B2. Stacked bar chart showing assignment impact across year of study.")

    st.markdown(
        """
**Interpretation (B2).** If higher year groups contain larger ‘major impact’ segments, it suggests increasing workload and time pressure.
This can promote late-night study behaviour and worsen sleep, creating a feedback loop that affects academic productivity.
"""
    )

    st.markdown("---")

    # =========================
    # B3 Scatter — ISI vs SleepHours_est (color by GPA)
    # =========================
    fig = px.scatter(
        df,
        x="SleepHours_est",
        y="InsomniaSeverity_index",
        color="GPA",
        title="Insomnia Severity vs Sleep Duration (Colored by GPA)",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B3. Scatter plot of insomnia severity against sleep duration, colored by GPA band.")

    st.markdown(
        """
**Interpretation (B3).** A trend where shorter sleep corresponds to higher insomnia severity indicates that students may be sleep-restricted
while simultaneously experiencing insomnia symptoms. Coloring by GPA helps evaluate whether high-achieving students are also exposed to poor sleep health.
"""
    )

    st.markdown("---")

    # =========================
    # B4 Treemap — Academic performance self-rating
    # =========================
    fig = px.treemap(df, path=["AcademicPerformance"], title="Self-Rated Academic Performance Composition")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B4. Treemap summarizing self-rated academic performance categories.")

    excellent = df["AcademicPerformance"].astype(str).str.contains("Excellent|Very good", na=False).sum()
    st.markdown(
        f"""
**Interpretation (B4).** The treemap shows perceived performance distribution. **{excellent} students ({pct(excellent,total):.1f}%)** rated themselves as excellent/very good.
Differences between self-perception and GPA bands may reflect fatigue, stress, and reduced confidence associated with poor sleep.
"""
    )

    st.markdown("---")

    # =========================
    # B5 Line — responses over time
    # =========================
    df_time = df.copy()
    df_time["Date"] = pd.to_datetime(df_time["Timestamp"], errors="coerce").dt.date
    ts = df_time.groupby("Date").size().reset_index(name="Responses")

    fig = px.line(ts, x="Date", y="Responses", markers=True, title="Survey Responses Over Time")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure B5. Line chart showing number of survey responses per day.")

    st.markdown(
        """
**Interpretation (B5).** The response trend indicates how data collection evolved over time. A consistent pattern supports dataset stability
and reduces the chance that findings are driven by a single-day response spike or unusual event period.
"""
    )


render()
