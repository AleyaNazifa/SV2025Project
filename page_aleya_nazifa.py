import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from data_loader import display_sidebar_info, get_df

def render():
    display_sidebar_info()
    
    df = get_df()
    
    if df is None:
        st.error("Failed to load data.")
        return
    
    st.title("📚 Academic Impact Analysis")
    st.markdown("### How Sleep Affects Academic Performance & Student Success")
    st.markdown("---")
    
    # Key Academic Impact Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        major_impact = df['AssignmentImpact'].str.contains('Major|Significant', na=False).sum()
        st.metric("Major Assignment Impact", f"{major_impact}",
                 f"{major_impact/len(df)*100:.1f}%",
                 delta_color="inverse")
    
    with col2:
        missed = df['MissedClasses'].str.contains('Sometimes|Often|Always', na=False).sum()
        st.metric("Missed Classes", f"{missed}",
                 f"{missed/len(df)*100:.1f}%",
                 delta_color="inverse")
    
    with col3:
        fatigue = df['DaytimeFatigue'].str.contains('Often|Always', na=False).sum()
        st.metric("Chronic Fatigue", f"{fatigue}",
                 f"{fatigue/len(df)*100:.1f}%",
                 delta_color="inverse")
    
    with col4:
        concentration = df['ConcentrationDifficulty'].str.contains('Often|Always', na=False).sum()
        st.metric("Concentration Issues", f"{concentration}",
                 f"{concentration/len(df)*100:.1f}%",
                 delta_color="inverse")
    
    st.markdown("---")
    
    # GPA vs Insomnia Analysis
    st.markdown("#### 📊 GPA Distribution by Insomnia Severity")
    
    def categorize_isi(score):
        if score < 8:
            return "No Insomnia"
        elif score < 15:
            return "Subthreshold"
        elif score < 22:
            return "Moderate"
        else:
            return "Severe"
    
    df['ISI_Category'] = df['InsomniaSeverity_index'].apply(categorize_isi)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # GPA distribution
        gpa_counts = df['GPA'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_gpa = plt.cm.Spectral(np.linspace(0.1, 0.9, len(gpa_counts)))
        gpa_counts.plot(kind='barh', ax=ax, color=colors_gpa, edgecolor='black')
        ax.set_xlabel('Number of Students', fontsize=11, fontweight='bold')
        ax.set_ylabel('GPA Range', fontsize=11, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        # CGPA distribution
        cgpa_counts = df['CGPA'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_cgpa = plt.cm.Viridis(np.linspace(0.2, 0.9, len(cgpa_counts)))
        cgpa_counts.plot(kind='barh', ax=ax, color=colors_cgpa, edgecolor='black')
        ax.set_xlabel('Number of Students', fontsize=11, fontweight='bold')
        ax.set_ylabel('CGPA Range', fontsize=11, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    # Correlation insight
    high_gpa = df['GPA'].str.contains('3.70|4.00', na=False)
    high_isi = df['InsomniaSeverity_index'] >= 15
    
    high_gpa_with_insomnia = (high_gpa & high_isi).sum()
    
    st.info(f"""
    🎯 **Key Finding:** 
    - **{high_gpa_with_insomnia}** high-achieving students (GPA ≥3.70) also have clinical insomnia (ISI≥15)
    - This represents **{high_gpa_with_insomnia/high_gpa.sum()*100:.1f}%** of all high-achieving students
    - Suggests that academic success may come at the cost of sleep health
    """)
    
    st.markdown("---")
    
    # Academic Performance Self-Rating
    st.markdown("#### 🎓 Self-Rated Academic Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        perf_counts = df['AcademicPerformance'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['#10b981', '#3b82f6', '#fbbf24', '#f97316', '#ef4444']
        perf_counts.plot(kind='bar', ax=ax, color=colors[:len(perf_counts)], edgecolor='black')
        ax.set_xlabel('Performance Rating', fontsize=11, fontweight='bold')
        ax.set_ylabel('Number of Students', fontsize=11, fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("**Performance Breakdown:**")
        for perf, count in perf_counts.items():
            pct = count / len(df) * 100
            st.metric(perf, f"{count}", f"{pct:.1f}%")
        
        excellent = df['AcademicPerformance'].str.contains('Excellent', na=False).sum()
        st.success(f"✨ **{excellent}** students rate their performance as Excellent!")
    
    st.markdown("---")
    
    # Sleep Impact on Academic Tasks
    st.markdown("#### 🎯 Sleep-Related Academic Challenges")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Concentration", "Fatigue", "Missed Classes", "Assignment Impact"
    ])
    
    with tab1:
        conc_counts = df['ConcentrationDifficulty'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        conc_counts.plot(kind='bar', ax=ax, color='#3b82f6', edgecolor='black')
        ax.set_xlabel('Frequency of Concentration Difficulty', fontsize=11, fontweight='bold')
        ax.set_ylabel('Number of Students', fontsize=11, fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        severe = df['ConcentrationDifficulty'].str.contains('Often|Always', na=False).sum()
        st.warning(f"⚠️ **{severe}** students ({severe/len(df)*100:.1f}%) have chronic concentration problems affecting their studies.")
    
    with tab2:
        fatigue_counts = df['DaytimeFatigue'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        fatigue_counts.plot(kind='bar', ax=ax, color='#f97316', edgecolor='black')
        ax.set_xlabel('Frequency of Daytime Fatigue', fontsize=11, fontweight='bold')
        ax.set_ylabel('Number of Students', fontsize=11, fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        chronic_fatigue = df['DaytimeFatigue'].str.contains('Often|Always', na=False).sum()
        st.error(f"🚨 **{chronic_fatigue}** students ({chronic_fatigue/len(df)*100:.1f}%) experience chronic daytime fatigue.")
    
    with tab3:
        missed_counts = df['MissedClasses'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        missed_counts.plot(kind='bar', ax=ax, color='#ef4444', edgecolor='black')
        ax.set_xlabel('Frequency of Missed Classes', fontsize=11, fontweight='bold')
        ax.set_ylabel('Number of Students', fontsize=11, fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        frequent_miss = df['MissedClasses'].str.contains('Sometimes|Often|Always', na=False).sum()
        if frequent_miss > 0:
            st.warning(f"📉 **{frequent_miss}** students have missed classes due to sleep issues.")
        else:
            st.success("✅ Most students maintain good class attendance despite sleep challenges!")
    
    with tab4:
        impact_counts = df['AssignmentImpact'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        colors_impact = ['#10b981', '#fbbf24', '#f97316', '#ef4444']
        impact_counts.plot(kind='bar', ax=ax, color=colors_impact[:len(impact_counts)], edgecolor='black')
        ax.set_xlabel('Impact on Assignments & Deadlines', fontsize=11, fontweight='bold')
        ax.set_ylabel('Number of Students', fontsize=11, fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        major = df['AssignmentImpact'].str.contains('Major|Significant', na=False).sum()
        st.error(f"📝 **{major}** students report significant impact on assignment completion.")
    
    st.markdown("---")
    
    # Exam Period Analysis
    st.markdown("#### 📖 Sleep Patterns During Exam Periods")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        exam_counts = df['ExamSleepChange'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_exam = ['#10b981', '#fbbf24', '#f97316', '#ef4444']
        exam_counts.plot(kind='barh', ax=ax, color=colors_exam[:len(exam_counts)], edgecolor='black')
        ax.set_xlabel('Number of Students', fontsize=11, fontweight='bold')
        ax.set_ylabel('Sleep Pattern Change', fontsize=11, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("**Exam Impact:**")
        
        severely_affected = df['ExamSleepChange'].str.contains('Significantly|Severely', na=False).sum()
        st.metric("Severely Affected", severely_affected, 
                 f"{severely_affected/len(df)*100:.1f}%",
                 delta_color="inverse")
        
        st.warning(f"""
        ⚠️ **Exam Stress Impact:**
        - **{severely_affected}** students experience severe sleep disruption during exams
        - This can create a vicious cycle affecting exam performance
        """)
    
    st.markdown("---")
    
    # Recommendations
    with st.expander("💡 Recommendations for Improving Academic Performance", expanded=True):
        st.markdown("""
        ### Evidence-Based Strategies:
        
        #### For Students:
        1. **Prioritize Sleep Schedule**: Maintain consistent bedtimes even during exam periods
        2. **Time Management**: Start assignments early to avoid all-nighters
        3. **Strategic Napping**: 20-30 minute power naps can boost concentration
        4. **Study Breaks**: Take regular breaks to prevent mental fatigue
        
        #### For Institutions:
        1. **Flexible Deadlines**: Consider sleep health when scheduling assignments
        2. **Sleep Education**: Workshops on sleep hygiene and time management
        3. **Mental Health Support**: Counseling for students with chronic sleep issues
        4. **Class Scheduling**: Avoid early morning classes when possible
        
        #### Warning Signs (Seek Help If):
        - Missing multiple classes due to sleep problems
        - Unable to concentrate despite adequate effort
        - Feeling constantly exhausted regardless of sleep duration
        - Academic performance declining despite best efforts
        """)

if __name__ == "__main__":
    render()
