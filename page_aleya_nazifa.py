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

    st.title("📚 Academic Impact Analysis")
    st.markdown("### How Sleep Affects Academic Performance & Student Success")
    st.markdown("---")

    # ======================
    # B1 — GPA Distribution
    # ======================
    st.markdown("#### 📊 GPA Distribution")
    if "GPA" in df.columns:
        gpa_counts = df["GPA"].value_counts(dropna=True)

        fig, ax = plt.subplots(figsize=(9, 4))
        gpa_counts.plot(kind="barh", ax=ax, edgecolor="black")
        ax.set_xlabel("Number of Students", fontsize=11, fontweight="bold")
        ax.set_ylabel("GPA Range", fontsize=11, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

        st.caption("Figure B1. Distribution of students by most recent semester GPA range.")

        high_gpa = df["GPA"].astype(str).str.contains("3.70|4.00", na=False).sum()
        st.markdown(
            f"""
**Interpretation (B1).** GPA distribution summarises overall academic performance in the sample. In this dataset, **{high_gpa} students ({_pct(high_gpa, total):.1f}%)**
fall within the highest GPA band (3.70–4.00). Comparing this distribution against sleep indicators helps assess whether strong academic outcomes coincide with sleep restriction
or insomnia symptoms within the same population.
"""
        )
    else:
        st.warning("GPA column not available.")

    st.markdown("---")

    # ======================
    # B2 — CGPA Distribution
    # ======================
    st.markdown("#### 📈 CGPA Distribution")
    if "CGPA" in df.columns:
        cgpa_counts = df["CGPA"].value_counts(dropna=True)

        fig, ax = plt.subplots(figsize=(9, 4))
        cgpa_counts.plot(kind="barh", ax=ax, edgecolor="black")
        ax.set_xlabel("Number of Students", fontsize=11, fontweight="bold")
        ax.set_ylabel("CGPA Range", fontsize=11, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

        st.caption("Figure B2. Distribution of students by cumulative GPA (CGPA) range.")

        st.markdown(
            f"""
**Interpretation (B2).** CGPA reflects longer-term performance across semesters and may be less sensitive to short-term fluctuations. The observed distribution helps identify
whether academic achievement is concentrated at certain CGPA bands. When cross-referenced with sleep disruption, CGPA can indicate whether chronic sleep issues correspond
to sustained academic difficulties or whether students maintain grades despite impaired sleep.
"""
        )
    else:
        st.warning("CGPA column not available.")

    st.markdown("---")

    # ======================
    # B3 — Self-rated Academic Performance
    # ======================
    st.markdown("#### 🎓 Self-Rated Academic Performance")
    if "AcademicPerformance" in df.columns:
        perf_counts = df["AcademicPerformance"].value_counts(dropna=True)

        fig, ax = plt.subplots(figsize=(10, 4))
        perf_counts.plot(kind="bar", ax=ax, edgecolor="black")
        ax.set_xlabel("Self-Rated Performance", fontsize=11, fontweight="bold")
        ax.set_ylabel("Number of Students", fontsize=11, fontweight="bold")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

        st.caption("Figure B3. Students’ self-rated academic performance in the past semester.")

        excellent = df["AcademicPerformance"].astype(str).str.contains("Excellent|Very good", na=False).sum()
        st.markdown(
            f"""
**Interpretation (B3).** Self-rated performance provides a subjective view that may capture motivation and perceived success beyond GPA alone. In this dataset, **{excellent}
students ({_pct(excellent, total):.1f}%)** rated their performance as excellent/very good. Divergence between self-rating and objective grades may reflect stress, workload,
or sleep-related cognitive impacts that reduce perceived effectiveness even when grades remain high.
"""
        )
    else:
        st.warning("AcademicPerformance column not available.")

    st.markdown("---")

    # ======================
    # B4 — Concentration Difficulty
    # ======================
    st.markdown("#### 🧠 Concentration Difficulty Due to Lack of Sleep")
    if "ConcentrationDifficulty" in df.columns:
        conc_counts = df["ConcentrationDifficulty"].value_counts(dropna=True)

        fig, ax = plt.subplots(figsize=(10, 4))
        conc_counts.plot(kind="bar", ax=ax, edgecolor="black")
        ax.set_xlabel("Frequency", fontsize=11, fontweight="bold")
        ax.set_ylabel("Number of Students", fontsize=11, fontweight="bold")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

        st.caption("Figure B4. Frequency of difficulty concentrating during lectures/study due to lack of sleep.")

        chronic = df["ConcentrationDifficulty"].astype(str).str.contains("Often|Always", na=False).sum()
        st.markdown(
            f"""
**Interpretation (B4).** Concentration is directly linked to sleep quality and total sleep time. Here, **{chronic} students ({_pct(chronic, total):.1f}%)** report chronic
concentration difficulty (often/always). Elevated rates suggest that sleep problems may be reducing attention span and learning efficiency, which can cascade into poorer
revision quality and reduced academic confidence.
"""
        )
    else:
        st.warning("ConcentrationDifficulty column not available.")

    st.markdown("---")

    # ======================
    # B5 — Assignment Impact
    # ======================
    st.markdown("#### 📝 Impact of Insufficient Sleep on Assignments and Deadlines")
    if "AssignmentImpact" in df.columns:
        impact_counts = df["AssignmentImpact"].value_counts(dropna=True)

        fig, ax = plt.subplots(figsize=(10, 4))
        impact_counts.plot(kind="bar", ax=ax, edgecolor="black")
        ax.set_xlabel("Impact Level", fontsize=11, fontweight="bold")
        ax.set_ylabel("Number of Students", fontsize=11, fontweight="bold")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

        st.caption("Figure B5. Reported impact of insufficient sleep on completing assignments and meeting deadlines.")

        major = df["AssignmentImpact"].astype(str).str.contains("Major|Significant", na=False).sum()
        st.markdown(
            f"""
**Interpretation (B5).** Assignment completion reflects time management and functional capacity under workload. In this dataset, **{major} students ({_pct(major, total):.1f}%)**
report major/significant impact. This suggests that insufficient sleep can reduce productivity, increase procrastination, and impair working memory—ultimately affecting the
ability to meet deadlines and sustain performance during high-demand periods.
"""
        )
    else:
        st.warning("AssignmentImpact column not available.")

    st.markdown("---")

    with st.expander("💡 Recommendations for Students & UMK", expanded=False):
        st.markdown(
            """
- Maintain consistent sleep schedule (avoid “all-nighters”).
- Start assignments earlier to reduce late-night work.
- Use short naps (20–30 minutes) strategically.
- Reduce screen time 60 minutes before bed.
- Seek counselling support if stress or insomnia persists.
"""
        )


render()
