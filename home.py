import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import display_sidebar_info, get_df


def pct(n, total):
    return (n / total * 100) if total else 0


def render():
    # Sidebar info
    display_sidebar_info()
    df = get_df()

    if df is None or len(df) == 0:
        st.error("No data available.")
        return

    total = len(df)

    # =========================
    # PAGE HEADER
    # =========================
    st.title("🎓 UMK Insomnia & Educational Outcomes Dashboard")
    st.markdown(
        "### An Interactive Visualization of Sleep Patterns, Academic Impact, and Lifestyle Factors"
    )

    st.markdown("---")

    # =========================
    # RESEARCH OBJECTIVES
    # =========================
    st.markdown("## 🎯 Research Objectives")

    st.markdown(
        """
1. **To analyze sleep patterns and insomnia severity** among UMK students by examining sleep duration, sleep quality, bedtime habits, and insomnia-related symptoms.

2. **To evaluate the impact of insufficient sleep on academic performance**, including concentration difficulties, fatigue, class attendance, and academic achievement indicators (GPA and self-rated performance).

3. **To investigate lifestyle and stress-related factors**—such as electronic device usage, caffeine consumption, physical activity, and academic stress—and their association with insomnia severity.
"""
    )

    st.markdown("---")

    # =========================
    # KEY METRICS
    # =========================
    st.markdown("## 📊 Key Summary Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Responses", f"{total:,}")

    with col2:
        if "SleepHours_est" in df:
            st.metric(
                "Avg Sleep Duration",
                f"{df['SleepHours_est'].mean():.2f} hours",
            )
        else:
            st.metric("Avg Sleep Duration", "N/A")

    with col3:
        if "InsomniaSeverity_index" in df:
            high_isi = (df["InsomniaSeverity_index"] >= 15).sum()
            st.metric(
                "High Insomnia Risk",
                f"{high_isi}",
                f"{pct(high_isi, total):.1f}%",
            )
        else:
            st.metric("High Insomnia Risk", "N/A")

    with col4:
        if "StressLevel" in df:
            high_stress = (
                df["StressLevel"]
                .astype(str)
                .str.contains("High|Extremely", na=False)
                .sum()
            )
            st.metric(
                "High Stress Levels",
                f"{high_stress}",
                f"{pct(high_stress, total):.1f}%",
            )
        else:
            st.metric("High Stress Levels", "N/A")

    st.markdown("---")

    # =========================
    # OVERVIEW VISUALIZATIONS
    # (NOT PART OF MEMBER MARKING)
    # =========================
    st.markdown("## 📈 Overall Data Overview")

    col_left, col_right = st.columns(2)

    # Insomnia Severity Distribution
    with col_left:
        if "InsomniaSeverity_index" in df:
            fig = px.histogram(
                df,
                x="InsomniaSeverity_index",
                nbins=10,
                title="Insomnia Severity Index (ISI) Distribution",
            )
            fig.update_layout(xaxis_title="ISI Score", yaxis_title="Number of Students")
            st.plotly_chart(fig, use_container_width=True)

            st.caption(
                "Figure O1. Distribution of insomnia severity index (ISI) scores among UMK students."
            )

    # Faculty Distribution
    with col_right:
        if "Faculty" in df:
            faculty_counts = (
                df["Faculty"].value_counts().head(10).reset_index()
            )
            faculty_counts.columns = ["Faculty", "Count"]

            fig = px.bar(
                faculty_counts,
                x="Count",
                y="Faculty",
                orientation="h",
                title="Top Faculties Represented in Survey",
            )
            fig.update_layout(
                xaxis_title="Number of Students",
                yaxis_title="Faculty",
            )
            st.plotly_chart(fig, use_container_width=True)

            st.caption(
                "Figure O2. Distribution of survey respondents across faculties (top 10)."
            )

    st.markdown("---")

    # =========================
    # RAW DATA PREVIEW
    # =========================
    with st.expander("📋 View Raw Survey Data", expanded=False):
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            label="📥 Download Dataset (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="umk_insomnia_survey_data.csv",
            mime="text/csv",
        )


# Render page
render()
