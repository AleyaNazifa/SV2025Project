import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
from data_loader import display_sidebar_info, get_df


def parse_sleep_hours(series: pd.Series) -> float:
    """
    Converts strings like:
    - "7–8 hours" -> 7.5
    - "5–6 hours" -> 5.5
    - "More than 8 hours" -> 8.5
    - "Less than 5 hours" -> 4.5
    Returns mean float.
    """
    def to_num(x: str):
        s = str(x)
        s = s.replace("–", "-").lower().strip()

        if "more than" in s:
            nums = re.findall(r"\d+", s)
            return float(nums[0]) + 0.5 if nums else np.nan

        if "less than" in s:
            nums = re.findall(r"\d+", s)
            return float(nums[0]) - 0.5 if nums else np.nan

        m = re.findall(r"\d+", s)
        if len(m) >= 2:
            a, b = float(m[0]), float(m[1])
            return (a + b) / 2
        if len(m) == 1:
            return float(m[0])
        return np.nan

    vals = series.dropna().map(to_num)
    return float(vals.mean()) if len(vals) else np.nan


def render():
    display_sidebar_info()
    df = get_df()

    if df is None or len(df) == 0:
        st.error("Failed to load data. Please check your Google Sheet link.")
        return

    st.title("🎓 UMK Insomnia & Educational Outcomes Dashboard")
    st.markdown("### Comprehensive Analysis of Sleep Patterns and Academic Performance")
    st.markdown("---")

    # Metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Responses", f"{len(df):,}")

    with col2:
        avg_sleep = parse_sleep_hours(df["SleepHours"]) if "SleepHours" in df.columns else np.nan
        if np.isnan(avg_sleep):
            st.metric("Avg Sleep Hours", "N/A")
        else:
            st.metric("Avg Sleep Hours", f"{avg_sleep:.1f}h", delta=f"{avg_sleep - 7:.1f}h vs recommended")

    with col3:
        if "InsomniaSeverity_index" in df.columns:
            high_isi = (df["InsomniaSeverity_index"] >= 15).sum()
            pct = high_isi / len(df) * 100
            st.metric("High Insomnia Risk", f"{high_isi}", delta=f"{pct:.1f}%", delta_color="inverse")
        else:
            st.metric("High Insomnia Risk", "N/A")

    with col4:
        if "GPA" in df.columns:
            high_gpa = df["GPA"].astype(str).str.contains("3.70|4.00", na=False).sum()
            pct_gpa = high_gpa / len(df) * 100
            st.metric("High GPA Students", f"{high_gpa}", delta=f"{pct_gpa:.1f}%")
        else:
            st.metric("High GPA Students", "N/A")

    with col5:
        if "StressLevel" in df.columns:
            high_stress = df["StressLevel"].astype(str).str.contains("High|Extremely high", na=False).sum()
            pct_stress = high_stress / len(df) * 100
            st.metric("High Stress", f"{high_stress}", delta=f"{pct_stress:.1f}%", delta_color="inverse")
        else:
            st.metric("High Stress", "N/A")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 😴 Insomnia Severity Distribution")

        if "InsomniaSeverity_index" in df.columns:
            def categorize_isi(score):
                if score < 8:
                    return "No Insomnia (0-7)"
                elif score < 15:
                    return "Subthreshold (8-14)"
                elif score < 22:
                    return "Moderate (15-21)"
                else:
                    return "Severe (22-28)"

            df_plot = df.copy()
            df_plot["ISI_Category"] = df_plot["InsomniaSeverity_index"].apply(categorize_isi)
            isi_counts = df_plot["ISI_Category"].value_counts()

            fig, ax = plt.subplots(figsize=(8, 5))
            isi_counts.plot(kind="bar", ax=ax, edgecolor="black")
            ax.set_xlabel("Insomnia Severity")
            ax.set_ylabel("Number of Students")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
            ax.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

            st.info(
                f"""
                📊 **Key Insights:**
                - Average ISI Score: **{df_plot['InsomniaSeverity_index'].mean():.1f}**
                - Median ISI Score: **{df_plot['InsomniaSeverity_index'].median():.1f}**
                - Students needing intervention (ISI≥15): **{((df_plot['InsomniaSeverity_index'] >= 15).sum() / len(df_plot) * 100):.1f}%**
                """
            )
        else:
            st.warning("InsomniaSeverity_index is not available yet.")

    with col_right:
        st.markdown("#### 🎯 Academic Performance Overview")

        if "GPA" in df.columns:
            gpa_order = ["Below 2.00", "2.00 - 2.49", "2.50 - 2.99", "3.00 - 3.49", "3.50 - 3.69", "3.70 - 4.00"]
            gpa_counts = df["GPA"].value_counts()
            gpa_counts_ordered = gpa_counts.reindex([g for g in gpa_order if g in gpa_counts.index], fill_value=0)

            fig, ax = plt.subplots(figsize=(8, 5))
            gpa_counts_ordered.plot(kind="bar", ax=ax, edgecolor="black")
            ax.set_xlabel("GPA Range")
            ax.set_ylabel("Number of Students")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
            ax.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

            excellent = df["AcademicPerformance"].astype(str).str.contains("Excellent|Very good", na=False).sum() if "AcademicPerformance" in df.columns else 0
            st.success(
                f"""
                🎓 **Academic Highlights:**
                - Students with GPA ≥ 3.50: **{df['GPA'].astype(str).str.contains('3.50|3.70|4.00', na=False).sum()}**
                - Self-rated excellent/very good: **{excellent}** ({excellent/len(df)*100:.1f}%)
                """
            )
        else:
            st.warning("GPA column not available.")

    st.markdown("---")
    st.markdown("#### 👥 Demographics & Faculty Distribution")

    col1, col2, col3 = st.columns(3)

    with col1:
        if "Gender" in df.columns:
            st.markdown("**Gender Distribution**")
            gender_counts = df["Gender"].value_counts()
            for gender, count in gender_counts.items():
                pct = count / len(df) * 100
                st.metric(str(gender), f"{count}", f"{pct:.1f}%")

    with col2:
        if "YearOfStudy" in df.columns:
            st.markdown("**Year of Study**")
            year_counts = df["YearOfStudy"].value_counts()
            for year, count in year_counts.items():
                pct = count / len(df) * 100
                st.write(f"**{year}**: {count} ({pct:.1f}%)")

    with col3:
        if "Faculty" in df.columns:
            st.markdown("**Top Faculties**")
            faculty_counts = df["Faculty"].value_counts().head(3)
            for faculty, count in faculty_counts.items():
                short = faculty.split("(")[-1].replace(")", "") if "(" in faculty else faculty[:15]
                st.write(f"**{short}**: {count}")

    st.markdown("---")

    with st.expander("📋 View Raw Data", expanded=False):
        st.dataframe(df.head(50), use_container_width=True, hide_index=True)
        st.download_button(
            label="📥 Download Full Dataset (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=f"umk_insomnia_data_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )


render()
