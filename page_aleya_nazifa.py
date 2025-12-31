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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        major_impact = df["AssignmentImpact"].astype(str).str.contains("Major|Significant", na=False).sum() if "AssignmentImpact" in df.columns else 0
        st.metric("Major Assignment Impact", f"{major_impact}", f"{major_impact/len(df)*100:.1f}%", delta_color="inverse")

    with col2:
        missed = df["MissedClasses"].astype(str).str.contains("Sometimes|Often|Always", na=False).sum() if "MissedClasses" in df.columns else 0
        st.metric("Missed Classes", f"{missed}", f"{missed/len(df)*100:.1f}%", delta_color="inverse")

    with col3:
        fatigue = df["DaytimeFatigue"].astype(str).str.contains("Often|Always", na=False).sum() if "DaytimeFatigue" in df.columns else 0
        st.metric("Chronic Fatigue", f"{fatigue}", f"{fatigue/len(df)*100:.1f}%", delta_color="inverse")

    with col4:
        concentration = df["ConcentrationDifficulty"].astype(str).str.contains("Often|Always", na=False).sum() if "ConcentrationDifficulty" in df.columns else 0
        st.metric("Concentration Issues", f"{concentration}", f"{concentration/len(df)*100:.1f}%", delta_color="inverse")

    st.markdown("---")
    st.markdown("#### 📊 GPA and CGPA Distributions")

    col1, col2 = st.columns(2)

    with col1:
        if "GPA" in df.columns:
            gpa_counts = df["GPA"].value_counts()
            fig, ax = plt.subplots(figsize=(8, 5))
            gpa_counts.plot(kind="barh", ax=ax, edgecolor="black")
            ax.set_xlabel("Number of Students")
            ax.set_ylabel("GPA Range")
            ax.grid(axis="x", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

    with col2:
        if "CGPA" in df.columns:
            cgpa_counts = df["CGPA"].value_counts()
            fig, ax = plt.subplots(figsize=(8, 5))
            cgpa_counts.plot(kind="barh", ax=ax, edgecolor="black")
            ax.set_xlabel("Number of Students")
            ax.set_ylabel("CGPA Range")
            ax.grid(axis="x", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

    st.markdown("---")
    st.markdown("#### 🎓 Self-Rated Academic Performance")

    if "AcademicPerformance" in df.columns:
        perf_counts = df["AcademicPerformance"].value_counts()
        fig, ax = plt.subplots(figsize=(9, 4))
        perf_counts.plot(kind="bar", ax=ax, edgecolor="black")
        ax.set_xlabel("Performance Rating")
        ax.set_ylabel("Number of Students")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("---")
    st.markdown("#### 🎯 Sleep-Related Academic Challenges")

    tab1, tab2, tab3, tab4 = st.tabs(["Concentration", "Fatigue", "Missed Classes", "Assignment Impact"])

    with tab1:
        if "ConcentrationDifficulty" in df.columns:
            conc_counts = df["ConcentrationDifficulty"].value_counts()
            fig, ax = plt.subplots(figsize=(10, 4))
            conc_counts.plot(kind="bar", ax=ax, edgecolor="black")
            ax.set_xlabel("Frequency")
            ax.set_ylabel("Count")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
            ax.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

    with tab2:
        if "DaytimeFatigue" in df.columns:
            fatigue_counts = df["DaytimeFatigue"].value_counts()
            fig, ax = plt.subplots(figsize=(10, 4))
            fatigue_counts.plot(kind="bar", ax=ax, edgecolor="black")
            ax.set_xlabel("Frequency")
            ax.set_ylabel("Count")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
            ax.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

    with tab3:
        if "MissedClasses" in df.columns:
            missed_counts = df["MissedClasses"].value_counts()
            fig, ax = plt.subplots(figsize=(10, 4))
            missed_counts.plot(kind="bar", ax=ax, edgecolor="black")
            ax.set_xlabel("Frequency")
            ax.set_ylabel("Count")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
            ax.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

    with tab4:
        if "AssignmentImpact" in df.columns:
            impact_counts = df["AssignmentImpact"].value_counts()
            fig, ax = plt.subplots(figsize=(10, 4))
            impact_counts.plot(kind="bar", ax=ax, edgecolor="black")
            ax.set_xlabel("Impact Level")
            ax.set_ylabel("Count")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
            ax.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

    st.markdown("---")
    st.markdown("#### 📖 Exam Period Sleep Changes")

    if "ExamSleepChange" in df.columns:
        exam_counts = df["ExamSleepChange"].value_counts()
        fig, ax = plt.subplots(figsize=(9, 4))
        exam_counts.plot(kind="barh", ax=ax, edgecolor="black")
        ax.set_xlabel("Number of Students")
        ax.set_ylabel("Sleep Pattern Change")
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

    with st.expander("💡 Recommendations for Students & UMK", expanded=True):
        st.markdown(
            """
            ### Strategies to Improve Academic Performance via Better Sleep
            
            **For Students**
            - Maintain consistent sleep schedule, even during exams
            - Avoid last-minute studying; plan earlier
            - Use short power naps (20–30 minutes)
            - Reduce screen time before bed
            
            **For UMK / Faculty**
            - Sleep hygiene campaigns and workshops
            - Time management & mental health support
            - Balanced assignment scheduling during exam weeks
            """
        )


render()
