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

    st.title("📚 Academic Impact Analysis")
    st.markdown("### How Sleep Affects Academic Performance & Student Success")
    st.markdown("---")

    # =========================
    # Key Academic Impact Metrics
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        major_impact = (
            df["AssignmentImpact"].astype(str).str.contains("Major|Significant", na=False).sum()
            if "AssignmentImpact" in df.columns
            else 0
        )
        st.metric(
            "Major Assignment Impact",
            f"{major_impact}",
            f"{(major_impact / len(df) * 100):.1f}%" if len(df) else "0.0%",
            delta_color="inverse",
        )

    with col2:
        missed = (
            df["MissedClasses"].astype(str).str.contains("Sometimes|Often|Always", na=False).sum()
            if "MissedClasses" in df.columns
            else 0
        )
        st.metric(
            "Missed Classes",
            f"{missed}",
            f"{(missed / len(df) * 100):.1f}%" if len(df) else "0.0%",
            delta_color="inverse",
        )

    with col3:
        fatigue = (
            df["DaytimeFatigue"].astype(str).str.contains("Often|Always", na=False).sum()
            if "DaytimeFatigue" in df.columns
            else 0
        )
        st.metric(
            "Chronic Fatigue",
            f"{fatigue}",
            f"{(fatigue / len(df) * 100):.1f}%" if len(df) else "0.0%",
            delta_color="inverse",
        )

    with col4:
        concentration = (
            df["ConcentrationDifficulty"].astype(str).str.contains("Often|Always", na=False).sum()
            if "ConcentrationDifficulty" in df.columns
            else 0
        )
        st.metric(
            "Concentration Issues",
            f"{concentration}",
            f"{(concentration / len(df) * 100):.1f}%" if len(df) else "0.0%",
            delta_color="inverse",
        )

    st.markdown("---")

    # =========================
    # ISI Category for analysis (optional)
    # =========================
    if "InsomniaSeverity_index" in df.columns:
        def categorize_isi(score):
            if score < 8:
                return "No Insomnia"
            elif score < 15:
                return "Subthreshold"
            elif score < 22:
                return "Moderate"
            else:
                return "Severe"

        df = df.copy()
        df["ISI_Category"] = df["InsomniaSeverity_index"].apply(categorize_isi)

    # =========================
    # GPA vs CGPA Distributions
    # =========================
    st.markdown("#### 📊 GPA and CGPA Distributions")
    colA, colB = st.columns(2)

    with colA:
        if "GPA" in df.columns:
            gpa_counts = df["GPA"].value_counts(dropna=True)

            fig, ax = plt.subplots(figsize=(8, 5))
            cmap = plt.get_cmap("Spectral")
            colors_gpa = cmap(np.linspace(0.1, 0.9, len(gpa_counts))) if len(gpa_counts) else None

            gpa_counts.plot(kind="barh", ax=ax, color=colors_gpa, edgecolor="black")
            ax.set_xlabel("Number of Students", fontsize=11, fontweight="bold")
            ax.set_ylabel("GPA Range", fontsize=11, fontweight="bold")
            ax.grid(axis="x", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("GPA column not available.")

    with colB:
        if "CGPA" in df.columns:
            cgpa_counts = df["CGPA"].value_counts(dropna=True)

            fig, ax = plt.subplots(figsize=(8, 5))

            # ✅ FIXED: Viridis must be lowercase, and using get_cmap is most robust
            cmap = plt.get_cmap("viridis")
            colors_cgpa = cmap(np.linspace(0.2, 0.9, len(cgpa_counts))) if len(cgpa_counts) else None

            cgpa_counts.plot(kind="barh", ax=ax, color=colors_cgpa, edgecolor="black")
            ax.set_xlabel("Number of Students", fontsize=11, fontweight="bold")
            ax.set_ylabel("CGPA Range", fontsize=11, fontweight="bold")
            ax.grid(axis="x", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("CGPA column not available.")

    # =========================
    # Quick Insight (GPA >= 3.70 with ISI >= 15)
    # =========================
    if "GPA" in df.columns and "InsomniaSeverity_index" in df.columns:
        high_gpa = df["GPA"].astype(str).str.contains("3.70|4.00", na=False)
        high_isi = df["InsomniaSeverity_index"] >= 15

        high_gpa_total = int(high_gpa.sum())
        high_gpa_with_insomnia = int((high_gpa & high_isi).sum())
        pct = (high_gpa_with_insomnia / high_gpa_total * 100) if high_gpa_total else 0.0

        st.info(
            f"""
            🎯 **Key Finding:**  
            - **{high_gpa_with_insomnia}** high-achieving students (GPA ≥ 3.70) also have clinical insomnia (ISI ≥ 15)  
            - This represents **{pct:.1f}%** of all high-achieving students
            """
        )

    st.markdown("---")

    # =========================
    # Self-rated Academic Performance
    # =========================
    st.markdown("#### 🎓 Self-Rated Academic Performance")

    if "AcademicPerformance" in df.columns:
        perf_counts = df["AcademicPerformance"].value_counts(dropna=True)

        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots(figsize=(8, 5))
            cmap = plt.get_cmap("tab10")
            colors_perf = cmap(np.linspace(0, 1, len(perf_counts))) if len(perf_counts) else None

            perf_counts.plot(kind="bar", ax=ax, color=colors_perf, edgecolor="black")
            ax.set_xlabel("Performance Rating", fontsize=11, fontweight="bold")
            ax.set_ylabel("Number of Students", fontsize=11, fontweight="bold")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
            ax.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

        with col2:
            st.markdown("**Performance Breakdown:**")
            for perf, count in perf_counts.items():
                pct = (count / len(df) * 100) if len(df) else 0.0
                st.metric(str(perf), f"{count}", f"{pct:.1f}%")

            excellent = df["AcademicPerformance"].astype(str).str.contains("Excellent|Very good", na=False).sum()
            st.success(f"✨ **{excellent}** students rate their performance as Excellent/Very good!")
    else:
        st.warning("AcademicPerformance column not available.")

    st.markdown("---")

    # =========================
    # Academic Challenges Tabs
    # =========================
    st.markdown("#### 🎯 Sleep-Related Academic Challenges")

    tab1, tab2, tab3, tab4 = st.tabs(["Concentration", "Fatigue", "Missed Classes", "Assignment Impact"])

    with tab1:
        if "ConcentrationDifficulty" in df.columns:
            conc_counts = df["ConcentrationDifficulty"].value_counts(dropna=True)
            fig, ax = plt.subplots(figsize=(10, 5))
            conc_counts.plot(kind="bar", ax=ax, color="#3b82f6", edgecolor="black")
            ax.set_xlabel("Frequency", fontsize=11, fontweight="bold")
            ax.set_ylabel("Number of Students", fontsize=11, fontweight="bold")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
            ax.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

            severe = df["ConcentrationDifficulty"].astype(str).str.contains("Often|Always", na=False).sum()
            st.warning(f"⚠️ **{severe}** students ({severe/len(df)*100:.1f}%) have chronic concentration problems.")
        else:
            st.warning("ConcentrationDifficulty column not available.")

    with tab2:
        if "DaytimeFatigue" in df.columns:
            fatigue_counts = df["DaytimeFatigue"].value_counts(dropna=True)
            fig, ax = plt.subplots(figsize=(10, 5))
            fatigue_counts.plot(kind="bar", ax=ax, color="#f97316", edgecolor="black")
            ax.set_xlabel("Frequency", fontsize=11, fontweight="bold")
            ax.set_ylabel("Number of Students", fontsize=11, fontweight="bold")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
            ax.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

            chronic = df["DaytimeFatigue"].astype(str).str.contains("Often|Always", na=False).sum()
            st.error(f"🚨 **{chronic}** students ({chronic/len(df)*100:.1f}%) experience chronic daytime fatigue.")
        else:
            st.warning("DaytimeFatigue column not available.")

    with tab3:
        if "MissedClasses" in df.columns:
            missed_counts = df["MissedClasses"].value_counts(dropna=True)
            fig, ax = plt.subplots(figsize=(10, 5))
            missed_counts.plot(kind="bar", ax=ax, color="#ef4444", edgecolor="black")
            ax.set_xlabel("Frequency", fontsize=11, fontweight="bold")
            ax.set_ylabel("Number of Students", fontsize=11, fontweight="bold")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
            ax.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

            frequent = df["MissedClasses"].astype(str).str.contains("Sometimes|Often|Always", na=False).sum()
            if frequent > 0:
                st.warning(f"📉 **{frequent}** students have missed classes due to sleep issues.")
            else:
                st.success("✅ Most students maintain good class attendance.")
        else:
            st.warning("MissedClasses column not available.")

    with tab4:
        if "AssignmentImpact" in df.columns:
            impact_counts = df["AssignmentImpact"].value_counts(dropna=True)
            fig, ax = plt.subplots(figsize=(10, 5))
            impact_counts.plot(kind="bar", ax=ax, color="#8b5cf6", edgecolor="black")
            ax.set_xlabel("Impact Level", fontsize=11, fontweight="bold")
            ax.set_ylabel("Number of Students", fontsize=11, fontweight="bold")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
            ax.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

            major = df["AssignmentImpact"].astype(str).str.contains("Major|Significant", na=False).sum()
            st.error(f"📝 **{major}** students report major impact on assignment completion.")
        else:
            st.warning("AssignmentImpact column not available.")

    st.markdown("---")

    # =========================
    # Exam Period Analysis
    # =========================
    st.markdown("#### 📖 Sleep Patterns During Exam Periods")

    if "ExamSleepChange" in df.columns:
        exam_counts = df["ExamSleepChange"].value_counts(dropna=True)

        colX, colY = st.columns([2, 1])

        with colX:
            fig, ax = plt.subplots(figsize=(8, 5))
            cmap = plt.get_cmap("plasma")
            colors_exam = cmap(np.linspace(0.2, 0.9, len(exam_counts))) if len(exam_counts) else None

            exam_counts.plot(kind="barh", ax=ax, color=colors_exam, edgecolor="black")
            ax.set_xlabel("Number of Students", fontsize=11, fontweight="bold")
            ax.set_ylabel("Sleep Pattern Change", fontsize=11, fontweight="bold")
            ax.grid(axis="x", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

        with colY:
            severely_affected = df["ExamSleepChange"].astype(str).str.contains("Significantly|Severely", na=False).sum()
            st.metric(
                "Severely Affected",
                severely_affected,
                f"{severely_affected/len(df)*100:.1f}%" if len(df) else "0.0%",
                delta_color="inverse",
            )

            st.warning(
                f"""
                ⚠️ **Exam Stress Impact:**
                - **{severely_affected}** students experience severe sleep disruption during exams
                - This can reduce concentration, memory, and performance
                """
            )
    else:
        st.warning("ExamSleepChange column not available.")

    st.markdown("---")

    # =========================
    # Recommendations
    # =========================
    with st.expander("💡 Recommendations for Improving Academic Performance", expanded=True):
        st.markdown(
            """
            ### Evidence-Based Strategies

            #### For Students
            1. Maintain consistent sleep schedule, even during exam periods
            2. Plan assignments early to avoid all-nighters
            3. Use strategic naps (20–30 minutes)
            4. Reduce screen time 1 hour before bed

            #### For UMK / Faculties
            1. Conduct sleep hygiene workshops
            2. Provide time-management support programs
            3. Strengthen counselling and mental health services
            4. Manage exam/assignment clustering and deadlines
            """
        )


render()
