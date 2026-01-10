import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

from data_loader import display_sidebar_info, get_df

pio.templates.default = "plotly_white"


# ==========================================
# Helper
# ==========================================
def pct(n, total):
    return (n / total * 100) if total else 0.0


# ==========================================
# Main Page
# ==========================================
def render():
    display_sidebar_info()

    df = get_df()
    if df is None or df.empty:
        st.error("No data available.")
        return

    total = len(df)

    st.title("Lifestyle & Stress Factors and Insomnia Severity")
    st.markdown(
        """
This dashboard examines how **lifestyle behaviours** (device usage, caffeine intake, physical activity)
and **academic stress** are associated with **insomnia severity** among university students.
        """
    )
    st.divider()

    # ==========================================
    # Key Metrics
    # ==========================================
    st.subheader("Key Lifestyle Risk Indicators")

    col1, col2, col3, col4 = st.columns(4)

    high_device = df["DeviceUsage"].astype(str).str.contains("Always|Often", na=False).sum()
    high_caffeine = df["CaffeineConsumption"].astype(str).str.contains("Always|Often", na=False).sum()
    low_activity = df["PhysicalActivity"].astype(str).str.contains("Never|Rarely", na=False).sum()
    high_stress = df["StressLevel"].astype(str).str.contains("High|Extremely", na=False).sum()

    col1.metric("📱 Frequent Device Use", f"{pct(high_device, total):.1f}%")
    col2.metric("☕ High Caffeine Intake", f"{pct(high_caffeine, total):.1f}%")
    col3.metric("🏃 Low Physical Activity", f"{pct(low_activity, total):.1f}%")
    col4.metric("🎓 High Academic Stress", f"{pct(high_stress, total):.1f}%")

    st.divider()

    # ==========================================
    # Figure C1 — Device Usage Distribution
    # ==========================================
    st.subheader("Figure C1 — Device Usage Before Sleep")

    device_counts = df["DeviceUsage"].value_counts().reset_index()
    device_counts.columns = ["DeviceUsage", "Count"]

    fig1 = px.bar(
        device_counts,
        x="DeviceUsage",
        y="Count",
        title="Distribution of Device Usage Before Sleep",
    )
    fig1.update_layout(
        xaxis_title="Device Usage Frequency",
        yaxis_title="Number of Students"
    )
    st.plotly_chart(fig1, use_container_width=True)

  st.markdown(
        """
**Key Insights**
- The bar chart shows that device usage before sleep is **not evenly distributed**.
- A visibly larger group of students reports using devices **often or always** compared to those who rarely or never use devices.
- This indicates that pre-bed screen exposure is a **common behaviour**, not a marginal one.

**Conclusion**
- Since frequent device use is widespread, it represents a **population-level risk factor**.
- Any association found later between device use and insomnia severity affects a **substantial portion of students**, increasing its practical importance.
        """
    )

    st.divider()

    # ==========================================
    # Figure C2 — Device Usage vs Insomnia Severity
    # ==========================================
    st.subheader("Figure C2 — Insomnia Severity by Device Usage")

    fig2 = px.box(
        df,
        x="DeviceUsage",
        y="InsomniaSeverity_index",
        title="Insomnia Severity Across Device Usage Levels",
    )
    fig2.update_layout(
        xaxis_title="Device Usage Before Sleep",
        yaxis_title="Insomnia Severity Index (ISI)"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        "**Interpretation:** Higher frequency of device usage is associated with higher insomnia severity scores, "
        "suggesting a negative impact of screen exposure on sleep health."
    )

    st.divider()

    # ==========================================
    # Figure C3 — Caffeine Consumption vs ISI
    # ==========================================
    st.subheader("Figure C3 — Insomnia Severity by Caffeine Consumption")

    fig3 = px.box(
        df,
        x="CaffeineConsumption",
        y="InsomniaSeverity_index",
        title="Insomnia Severity Across Caffeine Consumption Levels",
    )
    fig3.update_layout(
        xaxis_title="Caffeine Consumption Frequency",
        yaxis_title="Insomnia Severity Index (ISI)"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(
        "**Interpretation:** Students with higher caffeine intake tend to report increased insomnia severity, "
        "consistent with caffeine’s stimulant effects on sleep."
    )

    st.divider()

    # ==========================================
    # Figure C4 — Stress Level vs Insomnia Severity (Violin)
    # ==========================================
    st.subheader("Figure C4 — Insomnia Severity by Academic Stress Level")

    fig4 = px.violin(
        df,
        x="StressLevel",
        y="InsomniaSeverity_index",
        box=True,
        title="Insomnia Severity Across Academic Stress Levels",
    )
    fig4.update_layout(
        xaxis_title="Academic Stress Level",
        yaxis_title="Insomnia Severity Index (ISI)"
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown(
        "**Interpretation:** Insomnia severity increases with higher academic stress levels, "
        "highlighting stress as a key contributor to sleep disturbance."
    )

    st.divider()

    # ==========================================
    # Figure C5 — Lifestyle Risk Score vs ISI
    # ==========================================
    st.subheader("Figure C5 — Combined Lifestyle Risk vs Insomnia Severity")

    fig5 = px.scatter(
        df,
        x="Lifestyle_Risk",
        y="InsomniaSeverity_index",
        opacity=0.75,
        title="Lifestyle Risk Score vs Insomnia Severity",
    )
    fig5.update_layout(
        xaxis_title="Lifestyle Risk Score",
        yaxis_title="Insomnia Severity Index (ISI)"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown(
        "**Interpretation:** A positive relationship is observed where higher accumulated lifestyle risk "
        "corresponds to higher insomnia severity, indicating that sleep problems often result from multiple combined behaviours."
    )

    st.success(
        "Conclusion: Lifestyle behaviours and academic stress show consistent associations with insomnia severity, "
        "supporting integrated sleep health interventions for university students."
    )


render()
