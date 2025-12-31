import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
from data_loader import display_sidebar_info, get_df


def _pct(n: int, total: int) -> float:
    return (n / total * 100) if total else 0.0


def _parse_sleep_hours(series: pd.Series) -> pd.Series:
    """
    Convert strings like '7–8 hours' -> 7.5, 'More than 8 hours' -> 8.5, etc.
    Returns numeric Series.
    """
    def to_num(x: str):
        s = str(x).replace("–", "-").lower().strip()

        if "more than" in s:
            m = re.findall(r"\d+", s)
            return float(m[0]) + 0.5 if m else np.nan

        if "less than" in s:
            m = re.findall(r"\d+", s)
            return float(m[0]) - 0.5 if m else np.nan

        m = re.findall(r"\d+", s)
        if len(m) >= 2:
            return (float(m[0]) + float(m[1])) / 2
        if len(m) == 1:
            return float(m[0])
        return np.nan

    return series.dropna().map(to_num)


def render():
    display_sidebar_info()
    df = get_df()

    if df is None or len(df) == 0:
        st.error("Failed to load data.")
        return

    st.title("😴 Sleep Patterns Analysis")
    st.markdown("### Deep Dive into Student Sleep Behaviors and Quality")
    st.markdown("---")

    total = len(df)

    # ======================
    # KPI row (optional)
    # ======================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if "SleepHours" in df.columns:
            sleep_num = _parse_sleep_hours(df["SleepHours"])
            avg_sleep = float(sleep_num.mean()) if len(sleep_num) else np.nan
            st.metric("Avg Sleep Duration", "N/A" if np.isnan(avg_sleep) else f"{avg_sleep:.1f}h")
        else:
            st.metric("Avg Sleep Duration", "N/A")

    with col2:
        poor_quality = (df["SleepQuality"].astype(str).isin(["1", "2"])).sum() if "SleepQuality" in df.columns else 0
        st.metric("Poor Sleep Quality", poor_quality, f"{_pct(poor_quality, total):.1f}%")

    with col3:
        late_sleepers = df["BedTime"].astype(str).str.contains("After 12 AM", na=False).sum() if "BedTime" in df.columns else 0
        st.metric("Late Sleepers", late_sleepers, f"{_pct(late_sleepers, total):.1f}%")

    with col4:
        frequent_wakeups = df["NightWakeups"].astype(str).str.contains("Often|Always", na=False).sum() if "NightWakeups" in df.columns else 0
        st.metric("Frequent Wakeups", frequent_wakeups, f"{_pct(frequent_wakeups, total):.1f}%")

    st.markdown("---")

    # ======================
    # A1 — Sleep Duration Distribution
    # ======================
    st.markdown("#### 🛏️ Sleep Duration Distribution")
    if "SleepHours" in df.columns:
        sleep_counts = df["SleepHours"].value_counts(dropna=True)

        fig, ax = plt.subplots(figsize=(9, 4))
        sleep_counts.plot(kind="barh", ax=ax, edgecolor="black")
        ax.set_xlabel("Number of Students", fontsize=11, fontweight="bold")
        ax.set_ylabel("Sleep Duration Category", fontsize=11, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

        st.caption("Figure A1. Distribution of self-reported sleep duration among UMK students.")
        # Interpretation paragraph (auto-updating)
        adequate = df["SleepHours"].astype(str).str.contains("7–8|7-8|More than 8|9", na=False).sum()
        short_sleep = total - adequate
        st.markdown(
            f"""
**Interpretation (A1).** The distribution indicates how common short sleep is in the sample. In this dataset, **{short_sleep} students ({_pct(short_sleep, total):.1f}%)**
report sleeping under the typical recommended range, while **{adequate} students ({_pct(adequate, total):.1f}%)** report adequate sleep duration. A higher concentration
in shorter-duration categories suggests potential sleep restriction that may contribute to fatigue and academic difficulties.
"""
        )
    else:
        st.warning("SleepHours column not available.")

    st.markdown("---")

    # ======================
    # A2 — Sleep Quality Ratings
    # ======================
    st.markdown("#### ⭐ Sleep Quality Ratings")
    if "SleepQuality" in df.columns:
        quality_counts = df["SleepQuality"].astype(str).value_counts(dropna=True).sort_index()

        fig, ax = plt.subplots(figsize=(9, 4))
        quality_counts.plot(kind="bar", ax=ax, edgecolor="black")
        ax.set_xlabel("Sleep Quality Rating (1=Poor, 5=Excellent)", fontsize=11, fontweight="bold")
        ax.set_ylabel("Number of Students", fontsize=11, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

        st.caption("Figure A2. Distribution of perceived sleep quality ratings (1–5).")

        avg_quality = pd.to_numeric(df["SleepQuality"], errors="coerce").mean()
        poor = df["SleepQuality"].astype(str).isin(["1", "2"]).sum()
        good = df["SleepQuality"].astype(str).isin(["4", "5"]).sum()

        st.markdown(
            f"""
**Interpretation (A2).** Sleep quality is a key indicator of restorative sleep. The average rating is **{avg_quality:.2f}/5**, with **{poor} students ({_pct(poor, total):.1f}%)**
reporting poor sleep (ratings 1–2) and **{good} students ({_pct(good, total):.1f}%)** reporting good/excellent sleep (ratings 4–5). A larger low-rating segment
often signals fragmented sleep, stress, or behavioural factors (e.g., late-night device use) that can elevate insomnia risk.
"""
        )
    else:
        st.warning("SleepQuality column not available.")

    st.markdown("---")

    # ======================
    # A3 — Bedtime Patterns
    # ======================
    st.markdown("#### 🌙 Bedtime Patterns")
    if "BedTime" in df.columns:
        bedtime_counts = df["BedTime"].value_counts(dropna=True)

        fig, ax = plt.subplots(figsize=(10, 4))
        bedtime_counts.plot(kind="bar", ax=ax, edgecolor="black")
        ax.set_xlabel("Usual Weekday Bedtime", fontsize=11, fontweight="bold")
        ax.set_ylabel("Number of Students", fontsize=11, fontweight="bold")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

        st.caption("Figure A3. Distribution of typical weekday bedtime categories.")

        late = df["BedTime"].astype(str).str.contains("After 12 AM", na=False).sum()
        st.markdown(
            f"""
**Interpretation (A3).** Bedtime distribution provides a proxy for circadian timing and sleep hygiene. Here, **{late} students ({_pct(late, total):.1f}%)** report
going to bed after midnight, which can reduce total sleep time and misalign circadian rhythm—especially when morning classes require early waking. A higher proportion of
late bedtimes may also reflect academic workload and device use at night.
"""
        )
    else:
        st.warning("BedTime column not available.")

    st.markdown("---")

    # ======================
    # A4 — Difficulty Falling Asleep
    # ======================
    st.markdown("#### 🚨 Difficulty Falling Asleep")
    if "DifficultyFallingAsleep" in df.columns:
        diff_counts = df["DifficultyFallingAsleep"].value_counts(dropna=True)

        fig, ax = plt.subplots(figsize=(9, 4))
        diff_counts.plot(kind="barh", ax=ax, edgecolor="black")
        ax.set_xlabel("Number of Students", fontsize=11, fontweight="bold")
        ax.set_ylabel("Frequency", fontsize=11, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

        st.caption("Figure A4. Frequency of difficulty falling asleep at night.")

        frequent = df["DifficultyFallingAsleep"].astype(str).str.contains("Often|Always", na=False).sum()
        st.markdown(
            f"""
**Interpretation (A4).** Difficulty initiating sleep is a core insomnia symptom. In this sample, **{frequent} students ({_pct(frequent, total):.1f}%)** report frequent
difficulty (often/always). Elevated rates suggest possible hyperarousal, stress, or poor sleep hygiene (e.g., late-night screen exposure), which can lengthen sleep latency
and reduce overall sleep quality.
"""
        )
    else:
        st.warning("DifficultyFallingAsleep column not available.")

    st.markdown("---")

    # ======================
    # A5 — Night Wakeups
    # ======================
    st.markdown("#### 🌘 Night Wakeups (Sleep Fragmentation)")
    if "NightWakeups" in df.columns:
        wake_counts = df["NightWakeups"].value_counts(dropna=True)

        fig, ax = plt.subplots(figsize=(10, 4))
        wake_counts.plot(kind="bar", ax=ax, edgecolor="black")
        ax.set_xlabel("Frequency of Night Wakeups", fontsize=11, fontweight="bold")
        ax.set_ylabel("Number of Students", fontsize=11, fontweight="bold")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

        st.caption("Figure A5. Frequency of waking during the night and difficulty returning to sleep.")

        frequent_w = df["NightWakeups"].astype(str).str.contains("Often|Always", na=False).sum()
        st.markdown(
            f"""
**Interpretation (A5).** Night-time awakenings indicate sleep fragmentation, which reduces sleep efficiency even when total hours appear adequate. Here, **{frequent_w} students
({_pct(frequent_w, total):.1f}%)** report frequent awakenings. Persistent fragmentation can contribute to daytime sleepiness, reduced attention, and higher insomnia severity,
making it an important target for sleep hygiene and stress management interventions.
"""
        )
    else:
        st.warning("NightWakeups column not available.")

    st.markdown("---")

    # Optional: methods (not counted in 5 visuals)
    with st.expander("💡 Sleep Methods Used by Students", expanded=False):
        if "SleepMethods" in df.columns:
            methods = df["SleepMethods"].dropna().value_counts().head(10)
            if len(methods) > 0:
                for method, count in methods.items():
                    st.write(f"- **{method}** ({count} students)")
            else:
                st.info("Not enough data on sleep methods.")


render()
