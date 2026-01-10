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

    st.title("Lifestyle & Stress Factors Associated with Insomnia Severity")
    st.markdown(
        """
This dashboard investigates how **electronic device usage**, **caffeine consumption**, 
**physical activity**, and **academic stress** are associated with **insomnia severity** 
among university students.
        """
    )
    st.divider()

    # ==========================================
    # Key Risk Metrics
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
    # Figure C1 — Device Usage vs Insomnia Severity
    # ==========================================
    st.subheader("Figure C1 — Insomnia Severity by Device Usage")

    fig1 = px.box(
        df,
        x="DeviceUsage",
        y="InsomniaSeverity_index",
        title="Insomnia Severity Across Device Usage Levels",
    )
    fig1.update_layout(
        xaxis_title="Device Usage Before Sleep",
        yaxis_title="Insomnia Severity Index (ISI)"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown(
        """
**Interpretation:**  
Students reporting more frequent device usage before sleep tend to show **higher insomnia severity scores**. 
This supports existing evidence that screen exposure and cognitive stimulation delay sleep onset.
        """
    )

    st.divider()

    # ==========================================
    # Figure C2 — Caffeine Consumption vs ISI
    # ==========================================
    st.subheader("Figure C2 — Insomnia Severity by Caffeine Consumption")

    fig2 = px.box(
        df,
        x="CaffeineConsumption",
        y="InsomniaSeverity_index",
        title="Insomnia Severity Across Caffeine Consumption Levels",
    )
    fig2.update_layout(
        xaxis_title="Caffeine Consumption",
        yaxis_title="Insomnia Severity Index (ISI)"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        """
**Interpretation:**  
Higher caffeine consumption is associated with **greater insomnia severity**, likely due to 
caffeine’s stimulant effects on sleep latency and sleep depth.
        """
    )

    st.divider()

    # ==========================================
    # Figure C3 — Physical Activity vs ISI
    # ==========================================
    st.subheader("Figure C3 — Insomnia Severity by Physical Activity Level")

    fig3 = px.box(
        df,
        x="PhysicalActivity",
        y="InsomniaSeverity_index",
        title="Insomnia Severity Across Physical Activity Levels",
    )
    fig3.update_layout(
        xaxis_title="Physical Activity Frequency",
        yaxis_title="Insomnia Severity Index (ISI)"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(
        """
**Interpretation:**  
Students engaging in **regular physical activity** generally report **lower insomnia severity**, 
supporting exercise as a protective factor for sleep quality.
        """
    )

    st.divider()

    # ==========================================
    # Figure C4 — Stress Level vs Insomnia Severity
    # ==========================================
    st.subheader("Figure C4 — Insomnia Severity by Academic Stress Level")

    fig4 = px.box(
        df,
        x="StressLevel",
        y="InsomniaSeverity_index",
        title="Insomnia Severity Across Academic Stress Levels",
    )
    fig4.update_layout(
        xaxis_title="Academic Stress Level",
        yaxis_title="Insomnia Severity Index (ISI)"
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown(
        """
**Interpretation:**  
A clear gradient is observed where **higher academic stress** corresponds to **higher insomnia severity**, 
highlighting stress as a dominant driver of sleep disruption.
        """
    )

    st.divider()

    # ==========================================
    # Figure C5 — Combined Lifestyle Risk vs ISI
    # ==========================================
    st.subheader("Figure C5 — Combined Lifestyle Risk Score vs Insomnia Severity")

    fig5 = px.scatter(
        df,
        x="Lifestyle_Risk",
        y="InsomniaSeverity_index",
        trendline="ols",
        title="Accumulated Lifestyle Risk vs Insomnia Severity",
        opacity=0.75,
    )
    fig5.update_layout(
        xaxis_title="Lifestyle Risk Score",
        yaxis_title="Insomnia Severity Index (ISI)"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown(
        """
**Interpretation:**  
A positive association is observed between **accumulated lifestyle risk** and **insomnia severity**.  
This indicates that sleep problems often emerge from **multiple interacting behaviours**, rather than a single factor.
        """
    )

    st.success(
        "Overall conclusion: Lifestyle behaviours and academic stress show consistent associations "
        "with insomnia severity, supporting integrated sleep health interventions for students."
    )


render()
