import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import display_sidebar_info, get_df


def _pct(n: int, total: int) -> float:
    return (n / total * 100) if total else 0.0


def render():
    display_sidebar_info()

    df = get_df()
    if df is None or len(df) == 0:
        st.error("Failed to load data.")
        return

    total = len(df)

    st.title("🏃 Lifestyle Factors Analysis")
    st.markdown("### Technology, Caffeine, Exercise, and Stress Impact on Sleep")
    st.markdown("---")

    # ======================
    # C1 — Device usage
    # ======================
    st.markdown("#### 📱 Device Usage Before Sleep")
    if "DeviceUsage" in df.columns:
        device_counts = df["DeviceUsage"].value_counts(dropna=True)

        fig, ax = plt.subplots(figsize=(10, 4))
        device_counts.plot(kind="barh", ax=ax, edgecolor="black")
        ax.set_xlabel("Number of Students", fontsize=11, fontweight="bold")
        ax.set_ylabel("Device Usage Frequency", fontsize=11, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

        st.caption("Figure C1. Frequency of electronic device usage before going to sleep.")

        heavy = df["DeviceUsage"].astype(str).str.contains("Always|Often", na=False).sum()
        st.markdown(
            f"""
**Interpretation (C1).** High pre-sleep device use can disrupt sleep through blue-light exposure and cognitive stimulation. In this dataset, **{heavy} students ({_pct(heavy, total):.1f}%)**
report using devices often/always before sleep. This pattern may contribute to delayed bedtime, reduced melatonin release, and increased difficulty falling asleep.
"""
        )
    else:
        st.warning("DeviceUsage column not available.")

    st.markdown("---")

    # ======================
    # C2 — Caffeine consumption
    # ======================
    st.markdown("#### ☕ Caffeine Consumption Frequency")
    if "CaffeineConsumption" in df.columns:
        caffeine_counts = df["CaffeineConsumption"].value_counts(dropna=True)

        fig, ax = plt.subplots(figsize=(10, 4))
        caffeine_counts.plot(kind="bar", ax=ax, edgecolor="black")
        ax.set_xlabel("Caffeine Consumption Frequency", fontsize=11, fontweight="bold")
        ax.set_ylabel("Number of Students", fontsize=11, fontweight="bold")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

        st.caption("Figure C2. Frequency of caffeine consumption to stay awake or alert.")

        high_caff = df["CaffeineConsumption"].astype(str).str.contains("Always|Often", na=False).sum()
        st.markdown(
            f"""
**Interpretation (C2).** Caffeine intake can increase alertness but may impair sleep onset and sleep depth, particularly when consumed later in the day. Here, **{high_caff} students
({_pct(high_caff, total):.1f}%)** report high-frequency use (often/always), which could indicate reliance on stimulants to compensate for sleep debt and daytime fatigue.
"""
        )
    else:
        st.warning("CaffeineConsumption column not available.")

    st.markdown("---")

    # ======================
    # C3 — Physical activity
    # ======================
    st.markdown("#### 🏃 Physical Activity Level")
    if "PhysicalActivity" in df.columns:
        activity_counts = df["PhysicalActivity"].value_counts(dropna=True)

        fig, ax = plt.subplots(figsize=(10, 4))
        activity_counts.plot(kind="barh", ax=ax, edgecolor="black")
        ax.set_xlabel("Number of Students", fontsize=11, fontweight="bold")
        ax.set_ylabel("Physical Activity Frequency", fontsize=11, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

        st.caption("Figure C3. Distribution of physical activity/exercise frequency among respondents.")

        sedentary = df["PhysicalActivity"].astype(str).str.contains("Never|Rarely", na=False).sum()
        st.markdown(
            f"""
**Interpretation (C3).** Regular physical activity is associated with better sleep quality and stress regulation. In this dataset, **{sedentary} students ({_pct(sedentary, total):.1f}%)**
report being sedentary (never/rarely). Higher sedentary rates may correspond with poorer sleep outcomes and reduced resilience to academic stress.
"""
        )
    else:
        st.warning("PhysicalActivity column not available.")

    st.markdown("---")

    # ======================
    # C4 — Stress levels
    # ======================
    st.markdown("#### 😰 Academic Stress Level Distribution")
    if "StressLevel" in df.columns:
        stress_counts = df["StressLevel"].value_counts(dropna=True)

        fig, ax = plt.subplots(figsize=(7, 6))
        ax.pie(stress_counts, labels=stress_counts.index, autopct="%1.1f%%", startangle=90)
        ax.set_title("Stress Level Distribution", fontsize=12, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig)

        st.caption("Figure C4. Proportion of students by reported academic stress level.")

        high_stress = df["StressLevel"].astype(str).str.contains("High|Extremely high", na=False).sum()
        st.markdown(
            f"""
**Interpretation (C4).** Stress is a well-established contributor to insomnia via physiological and cognitive arousal. Here, **{high_stress} students ({_pct(high_stress, total):.1f}%)**
report high or extremely high stress. Elevated stress prevalence suggests that sleep interventions may need to include stress management and time-planning support.
"""
        )
    else:
        st.warning("StressLevel column not available.")

    st.markdown("---")

    # ======================
    # C5 — Lifestyle risk score histogram
    # ======================
    st.markdown("#### 🎯 Lifestyle Risk Score Distribution")

    def lifestyle_risk(row) -> int:
        risk = 0

        # Devices
        v = str(row.get("DeviceUsage", ""))
        if "Always" in v:
            risk += 3
        elif "Often" in v:
            risk += 2

        # Caffeine
        c = str(row.get("CaffeineConsumption", ""))
        if "Always" in c:
            risk += 3
        elif "Often" in c:
            risk += 2

        # Exercise (risk if inactive)
        p = str(row.get("PhysicalActivity", ""))
        if ("Never" in p) or ("Rarely" in p):
            risk += 2

        # Stress
        s = str(row.get("StressLevel", ""))
        if "Extremely high" in s:
            risk += 3
        elif "High" in s:
            risk += 2

        return risk

    df_plot = df.copy()
    df_plot["Lifestyle_Risk"] = df_plot.apply(lifestyle_risk, axis=1)

    fig, ax = plt.subplots(figsize=(10, 4))
    df_plot["Lifestyle_Risk"].hist(bins=12, ax=ax, edgecolor="black")
    ax.set_xlabel("Lifestyle Risk Score", fontsize=11, fontweight="bold")
    ax.set_ylabel("Number of Students", fontsize=11, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

    st.caption("Figure C5. Distribution of combined lifestyle risk score based on device use, caffeine, inactivity, and stress.")

    high_risk = (df_plot["Lifestyle_Risk"] > 6).sum()
    st.markdown(
        f"""
**Interpretation (C5).** The lifestyle risk score aggregates multiple behaviours that can jointly worsen sleep. In this dataset, **{high_risk} students ({_pct(high_risk, total):.1f}%)**
fall into the high-risk range (>6), indicating concurrent exposure to several adverse factors (e.g., frequent device use, high caffeine intake, inactivity, and high stress).
This supports a multi-component intervention approach rather than targeting only one behaviour.
"""
    )

    st.markdown("---")

    with st.expander("💡 Lifestyle Recommendations", expanded=False):
        st.markdown(
            """
- Implement a “digital curfew” 60 minutes before bedtime.
- Avoid caffeine after 2 PM (or 6+ hours before sleep).
- Add moderate activity (20–30 minutes daily).
- Apply stress strategies (breathing, planning, counselling).
"""
        )


render()
