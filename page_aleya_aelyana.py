import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
from data_loader import display_sidebar_info, get_df


def parse_sleep_hours(series: pd.Series) -> float:
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

    vals = series.dropna().map(to_num)
    return float(vals.mean()) if len(vals) else np.nan


def render():
    display_sidebar_info()
    df = get_df()

    if df is None or len(df) == 0:
        st.error("Failed to load data.")
        return

    st.title("😴 Sleep Patterns Analysis")
    st.markdown("### Deep Dive into Student Sleep Behaviors and Quality")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_sleep = parse_sleep_hours(df["SleepHours"]) if "SleepHours" in df.columns else np.nan
        st.metric("Avg Sleep Duration", "N/A" if np.isnan(avg_sleep) else f"{avg_sleep:.1f}h")

    with col2:
        poor_quality = (df["SleepQuality"].astype(str).isin(["1", "2"])).sum() if "SleepQuality" in df.columns else 0
        st.metric("Poor Sleep Quality", f"{poor_quality}", f"{poor_quality/len(df)*100:.1f}%", delta_color="inverse")

    with col3:
        late_sleepers = df["BedTime"].astype(str).str.contains("After 12 AM", na=False).sum() if "BedTime" in df.columns else 0
        st.metric("Late Sleepers (After 12 AM)", f"{late_sleepers}", f"{late_sleepers/len(df)*100:.1f}%", delta_color="inverse")

    with col4:
        frequent_wakeups = df["NightWakeups"].astype(str).str.contains("Often|Always", na=False).sum() if "NightWakeups" in df.columns else 0
        st.metric("Frequent Night Wakeups", f"{frequent_wakeups}", f"{frequent_wakeups/len(df)*100:.1f}%", delta_color="inverse")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 🛏️ Sleep Duration Distribution")
        if "SleepHours" in df.columns:
            sleep_counts = df["SleepHours"].value_counts()

            fig, ax = plt.subplots(figsize=(8, 5))
            sleep_counts.plot(kind="barh", ax=ax, edgecolor="black")
            ax.set_xlabel("Number of Students")
            ax.set_ylabel("Sleep Duration")
            ax.grid(axis="x", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("SleepHours column not available.")

    with col_right:
        st.markdown("#### ⭐ Sleep Quality Ratings")
        if "SleepQuality" in df.columns:
            quality_counts = df["SleepQuality"].astype(str).value_counts().sort_index()

            fig, ax = plt.subplots(figsize=(8, 5))
            quality_counts.plot(kind="bar", ax=ax, edgecolor="black")
            ax.set_xlabel("Sleep Quality Rating (1=Poor, 5=Excellent)")
            ax.set_ylabel("Number of Students")
            ax.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

            avg_quality = pd.to_numeric(df["SleepQuality"], errors="coerce").mean()
            good_quality = df["SleepQuality"].astype(str).isin(["4", "5"]).sum()
            st.success(
                f"""
                ⭐ **Sleep Quality Summary:**
                - Average rating: **{avg_quality:.2f}/5.0**
                - Good/Excellent (4-5): **{good_quality}** ({good_quality/len(df)*100:.1f}%)
                """
            )
        else:
            st.warning("SleepQuality column not available.")

    st.markdown("---")
    st.markdown("#### 🌙 Bedtime Patterns")

    if "BedTime" in df.columns:
        bedtime_counts = df["BedTime"].value_counts()

        fig, ax = plt.subplots(figsize=(9, 4))
        bedtime_counts.plot(kind="bar", ax=ax, edgecolor="black")
        ax.set_xlabel("Bedtime")
        ax.set_ylabel("Number of Students")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("---")
    st.markdown("#### 🚨 Sleep Difficulties & Disturbances")

    tab1, tab2, tab3 = st.tabs(["Falling Asleep", "Night Wakeups", "Daytime Napping"])

    with tab1:
        if "DifficultyFallingAsleep" in df.columns:
            counts = df["DifficultyFallingAsleep"].value_counts()
            fig, ax = plt.subplots(figsize=(8, 4))
            counts.plot(kind="barh", ax=ax, edgecolor="black")
            ax.set_xlabel("Number of Students")
            ax.set_ylabel("Frequency")
            ax.grid(axis="x", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

    with tab2:
        if "NightWakeups" in df.columns:
            counts = df["NightWakeups"].value_counts()
            fig, ax = plt.subplots(figsize=(10, 4))
            counts.plot(kind="bar", ax=ax, edgecolor="black")
            ax.set_xlabel("Frequency of Night Wakeups")
            ax.set_ylabel("Number of Students")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
            ax.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

    with tab3:
        if "DayNap" in df.columns:
            nap_counts = df["DayNap"].value_counts()

            fig, ax = plt.subplots(figsize=(7, 5))
            nap_counts.plot(kind="pie", ax=ax, autopct="%1.1f%%", startangle=90)
            ax.set_ylabel("")
            plt.tight_layout()
            st.pyplot(fig)

            # ✅ FIX: your values are Occasionally/Frequently/Never
            regular_nappers = df["DayNap"].astype(str).str.contains("Frequently|Occasionally", na=False).sum()
            st.info(f"Regular nappers (Occasionally/Frequently): **{regular_nappers}** ({regular_nappers/len(df)*100:.1f}%)")

    st.markdown("---")
    with st.expander("💡 Sleep Methods Used by Students", expanded=True):
        if "SleepMethods" in df.columns:
            methods = df["SleepMethods"].dropna().value_counts().head(10)
            if len(methods) > 0:
                for method, count in methods.items():
                    st.write(f"- **{method}** ({count} students)")
            else:
                st.info("Not enough data on sleep methods.")


render()
