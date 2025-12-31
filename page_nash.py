import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from data_loader import display_sidebar_info, get_df


def render():
    display_sidebar_info()
    df = get_df()

    if df is None or len(df) == 0:
        st.error("Failed to load data.")
        return

    st.title("🏃 Lifestyle Factors Analysis")
    st.markdown("### Technology, Caffeine, Exercise, and Stress Impact on Sleep")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        devices = df["DeviceUsage"].astype(str).str.contains("Always|Often", na=False).sum() if "DeviceUsage" in df.columns else 0
        st.metric("High Device Usage", f"{devices}", f"{devices/len(df)*100:.1f}%", delta_color="inverse")

    with col2:
        caffeine = df["CaffeineConsumption"].astype(str).str.contains("Always|Often", na=False).sum() if "CaffeineConsumption" in df.columns else 0
        st.metric("High Caffeine Users", f"{caffeine}", f"{caffeine/len(df)*100:.1f}%", delta_color="inverse")

    with col3:
        sedentary = df["PhysicalActivity"].astype(str).str.contains("Never|Rarely", na=False).sum() if "PhysicalActivity" in df.columns else 0
        st.metric("Sedentary Lifestyle", f"{sedentary}", f"{sedentary/len(df)*100:.1f}%", delta_color="inverse")

    with col4:
        high_stress = df["StressLevel"].astype(str).str.contains("High|Extremely high", na=False).sum() if "StressLevel" in df.columns else 0
        st.metric("High Stress Levels", f"{high_stress}", f"{high_stress/len(df)*100:.1f}%", delta_color="inverse")

    st.markdown("---")
    st.markdown("#### 📱 Device Usage Before Sleep")

    if "DeviceUsage" in df.columns:
        device_counts = df["DeviceUsage"].value_counts()
        fig, ax = plt.subplots(figsize=(9, 4))
        device_counts.plot(kind="barh", ax=ax, edgecolor="black")
        ax.set_xlabel("Count")
        ax.set_ylabel("Device Usage")
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("---")
    st.markdown("#### ☕ Caffeine Consumption")

    if "CaffeineConsumption" in df.columns:
        caffeine_counts = df["CaffeineConsumption"].value_counts()
        fig, ax = plt.subplots(figsize=(9, 4))
        caffeine_counts.plot(kind="bar", ax=ax, edgecolor="black")
        ax.set_xlabel("Frequency")
        ax.set_ylabel("Count")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("---")
    st.markdown("#### 🏃 Physical Activity")

    if "PhysicalActivity" in df.columns:
        activity_counts = df["PhysicalActivity"].value_counts()
        fig, ax = plt.subplots(figsize=(9, 4))
        activity_counts.plot(kind="barh", ax=ax, edgecolor="black")
        ax.set_xlabel("Count")
        ax.set_ylabel("Activity Level")
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("---")
    st.markdown("#### 😰 Stress Level Distribution")

    if "StressLevel" in df.columns:
        stress_counts = df["StressLevel"].value_counts()
        fig, ax = plt.subplots(figsize=(7, 6))
        ax.pie(stress_counts, labels=stress_counts.index, autopct="%1.1f%%", startangle=90)
        ax.set_title("Stress Level Distribution")
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("---")
    st.markdown("#### 🎯 Lifestyle Risk Score")

    def calculate_lifestyle_risk(row):
        risk = 0

        # Device usage
        if pd.notna(row.get("DeviceUsage")) and "Always" in str(row.get("DeviceUsage")):
            risk += 3
        elif pd.notna(row.get("DeviceUsage")) and "Often" in str(row.get("DeviceUsage")):
            risk += 2

        # Caffeine usage
        if pd.notna(row.get("CaffeineConsumption")) and "Always" in str(row.get("CaffeineConsumption")):
            risk += 3
        elif pd.notna(row.get("CaffeineConsumption")) and "Often" in str(row.get("CaffeineConsumption")):
            risk += 2

        # Exercise (risk if inactive)
        if pd.notna(row.get("PhysicalActivity")) and ("Never" in str(row.get("PhysicalActivity")) or "Rarely" in str(row.get("PhysicalActivity"))):
            risk += 2

        # Stress
        if pd.notna(row.get("StressLevel")) and "Extremely high" in str(row.get("StressLevel")):
            risk += 3
        elif pd.notna(row.get("StressLevel")) and "High" in str(row.get("StressLevel")):
            risk += 2

        return risk

    df_plot = df.copy()
    df_plot["Lifestyle_Risk"] = df_plot.apply(calculate_lifestyle_risk, axis=1)

    col1, col2, col3 = st.columns(3)
    with col1:
        low = (df_plot["Lifestyle_Risk"] <= 3).sum()
        st.metric("Low Risk", low, f"{low/len(df_plot)*100:.1f}%")
    with col2:
        mid = ((df_plot["Lifestyle_Risk"] > 3) & (df_plot["Lifestyle_Risk"] <= 6)).sum()
        st.metric("Moderate Risk", mid, f"{mid/len(df_plot)*100:.1f}%")
    with col3:
        high = (df_plot["Lifestyle_Risk"] > 6).sum()
        st.metric("High Risk", high, f"{high/len(df_plot)*100:.1f}%", delta_color="inverse")

    fig, ax = plt.subplots(figsize=(9, 4))
    df_plot["Lifestyle_Risk"].hist(bins=12, ax=ax, edgecolor="black")
    ax.set_xlabel("Lifestyle Risk Score")
    ax.set_ylabel("Number of Students")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

    st.info(
        """
        **Lifestyle Risk Score**
        - Device usage (Often/Always): +2 to +3
        - Caffeine (Often/Always): +2 to +3
        - Lack of exercise (Never/Rarely): +2
        - High stress: +2 to +3
        
        **Interpretation**
        - 0–3: Low risk
        - 4–6: Moderate risk
        - 7+: High risk
        """
    )

    with st.expander("💡 Lifestyle Recommendations", expanded=True):
        st.markdown(
            """
            ### Lifestyle Changes to Improve Sleep
            
            - Stop screen time 1 hour before bed
            - Avoid caffeine after 2 PM
            - Exercise regularly (20–30 minutes daily)
            - Stress management: breathing, meditation, counselling
            """
        )


render()
