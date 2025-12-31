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

    # C1 Bar — Device usage
    device_counts = df["DeviceUsage"].value_counts().reset_index()
    device_counts.columns = ["DeviceUsage", "Count"]
    fig = px.bar(device_counts, x="DeviceUsage", y="Count", title="Device Usage Before Sleep")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure C1. Bar chart of device usage frequency before bedtime.")
    heavy = df["DeviceUsage"].astype(str).str.contains("Always|Often", na=False).sum()
    st.markdown(
        f"**Interpretation (C1).** **{heavy} students ({pct(heavy,total):.1f}%)** report frequent device use, "
        "which may delay sleep onset through blue-light exposure and stimulation."
    )

    # C2 Radar — Risk profile (normalized proportions)
    risk = {
        "Device Use": (df["DeviceUsage"].astype(str).str.contains("Always|Often", na=False)).mean(),
        "Caffeine": (df["CaffeineConsumption"].astype(str).str.contains("Always|Often", na=False)).mean(),
        "Stress": (df["StressLevel"].astype(str).str.contains("High|Extremely", na=False)).mean(),
        "Inactivity": (df["PhysicalActivity"].astype(str).str.contains("Never|Rarely", na=False)).mean(),
    }
    radar_df = pd.DataFrame({"Factor": list(risk.keys()), "Score": list(risk.values())})
    fig = px.line_polar(radar_df, r="Score", theta="Factor", line_close=True, title="Average Lifestyle Risk Profile")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure C2. Radar chart summarizing prevalence of key lifestyle risks.")
    st.markdown(
        "**Interpretation (C2).** Larger values indicate more students exposed to that risk, suggesting where "
        "interventions may be most impactful (e.g., stress management or device reduction)."
    )

    # C3 Sunburst — Stress → Caffeine → Device
    fig = px.sunburst(df, path=["StressLevel", "CaffeineConsumption", "DeviceUsage"], title="Stress → Caffeine → Device Usage")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure C3. Sunburst showing how stress, caffeine, and device use co-occur.")
    st.markdown(
        "**Interpretation (C3).** High-stress groups may cluster with higher caffeine and device use, indicating "
        "compounding behaviours that increase sleep disruption risk."
    )

    # C4 Bubble — Lifestyle_Risk vs ISI
    fig = px.scatter(
        df,
        x="Lifestyle_Risk",
        y="InsomniaSeverity_index",
        size="Lifestyle_Risk",
        color="StressLevel",
        title="Lifestyle Risk vs Insomnia Severity",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure C4. Bubble plot of lifestyle risk score versus insomnia severity (colored by stress).")
    st.markdown(
        "**Interpretation (C4).** A rising pattern suggests higher cumulative lifestyle risk aligns with higher "
        "insomnia severity, supporting multi-factor behavioural interventions."
    )

    # C5 Heatmap — Device × Caffeine
    heat = pd.crosstab(df["DeviceUsage"], df["CaffeineConsumption"])
    fig = px.imshow(heat, text_auto=True, title="Device Usage vs Caffeine Consumption")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure C5. Heatmap of device usage frequency against caffeine consumption frequency.")
    st.markdown(
        "**Interpretation (C5).** Concentration of counts in higher device and higher caffeine categories indicates "
        "behavioural patterns that may jointly worsen sleep outcomes."
    )


render()
