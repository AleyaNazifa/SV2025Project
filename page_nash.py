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

    st.title("🏃 Lifestyle Factors Analysis")
    st.markdown("### Behavioural Contributors to Sleep Quality")
    st.markdown("---")

    # =========================
    # C1 Bar — Device usage
    # =========================
    fig = px.bar(
        df["DeviceUsage"].value_counts(),
        title="Device Usage Before Sleep"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure C1. Frequency of electronic device usage before sleep.")

    st.markdown(
        """
**Interpretation (C1).** Frequent device usage before bedtime may delay sleep onset
due to blue-light exposure and cognitive stimulation.
"""
    )

    # =========================
    # C2 Radar — Lifestyle risk profile
    # =========================
    risk = {
        "Device Use": (df["DeviceUsage"].str.contains("Always|Often", na=False)).mean(),
        "Caffeine": (df["CaffeineConsumption"].str.contains("Always|Often", na=False)).mean(),
        "Stress": (df["StressLevel"].str.contains("High|Extremely", na=False)).mean(),
        "Inactivity": (df["PhysicalActivity"].str.contains("Never|Rarely", na=False)).mean(),
    }

    radar_df = pd.DataFrame(dict(
        r=list(risk.values()),
        theta=list(risk.keys())
    ))

    fig = px.line_polar(
        radar_df,
        r="r",
        theta="theta",
        line_close=True,
        title="Average Lifestyle Risk Profile"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure C2. Radar chart of average lifestyle risk factors.")

    st.markdown(
        """
**Interpretation (C2).** Stress and device use show the strongest lifestyle risk signals,
suggesting these behaviours may play a major role in sleep disruption.
"""
    )

    # =========================
    # C3 Sunburst — Stress → caffeine → device
    # =========================
    fig = px.sunburst(
        df,
        path=["StressLevel", "CaffeineConsumption", "DeviceUsage"],
        title="Lifestyle Behaviour Hierarchy"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure C3. Sunburst chart linking stress, caffeine, and device use.")

    st.markdown(
        """
**Interpretation (C3).** The hierarchical structure shows how high stress often co-occurs
with increased caffeine intake and device usage, compounding sleep risk.
"""
    )

    # =========================
    # C4 Bubble — Lifestyle risk vs ISI
    # =========================
    fig = px.scatter(
        df,
        x="Lifestyle_Risk",
        y="InsomniaSeverity_index",
        size="Lifestyle_Risk",
        color="StressLevel",
        title="Lifestyle Risk vs Insomnia Severity"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure C4. Bubble chart of lifestyle risk score versus insomnia severity.")

    st.markdown(
        """
**Interpretation (C4).** Students with higher lifestyle risk scores generally show
higher insomnia severity, reinforcing the cumulative impact of multiple
behavioural factors.
"""
    )

    # =========================
    # C5 Heatmap — Device × caffeine
    # =========================
    heat = pd.crosstab(df["DeviceUsage"], df["CaffeineConsumption"])
    fig = px.imshow(
        heat,
        text_auto=True,
        title="Device Usage vs Caffeine Consumption"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure C5. Heatmap of device usage and caffeine consumption frequency.")

    st.markdown(
        """
**Interpretation (C5).** The heatmap reveals clustering of high device usage and high
caffeine intake, indicating behavioural patterns that may jointly worsen sleep quality.
"""
    )


render()
