import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import display_sidebar_info, get_df

def render():
    # Display sidebar info
    display_sidebar_info()
    
    df = get_df()
    
    if df is None:
        st.error("Failed to load data. Please check your connection.")
        return
    
    # Header
    st.title("🎓 UMK Insomnia & Educational Outcomes Dashboard")
    st.markdown("### Comprehensive Analysis of Sleep Patterns and Academic Performance")
    st.markdown("---")
    
    # Key Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Responses",
            f"{len(df):,}",
            delta=None,
            help="Total number of survey responses"
        )
    
    with col2:
        avg_sleep = df['SleepHours'].str.extract(r'(\d+)').astype(float).mean().values[0]
        st.metric(
            "Avg Sleep Hours",
            f"{avg_sleep:.1f}h",
            delta=f"{avg_sleep - 7:.1f}h vs recommended",
            help="Average sleep duration compared to recommended 7-9 hours"
        )
    
    with col3:
        high_isi = (df['InsomniaSeverity_index'] >= 15).sum()
        pct = (high_isi / len(df) * 100)
        st.metric(
            "High Insomnia Risk",
            f"{high_isi}",
            delta=f"{pct:.1f}%",
            delta_color="inverse",
            help="Students with ISI ≥ 15 (clinical insomnia)"
        )
    
    with col4:
        high_gpa = df['GPA'].str.contains('3.70|4.00', na=False).sum()
        pct_gpa = (high_gpa / len(df) * 100)
        st.metric(
            "High GPA Students",
            f"{high_gpa}",
            delta=f"{pct_gpa:.1f}%",
            help="Students with GPA ≥ 3.70"
        )
    
    with col5:
        high_stress = df['StressLevel'].str.contains('High|Very high', na=False).sum()
        pct_stress = (high_stress / len(df) * 100)
        st.metric(
            "High Stress",
            f"{high_stress}",
            delta=f"{pct_stress:.1f}%",
            delta_color="inverse",
            help="Students reporting high/very high stress"
        )
    
    st.markdown("---")
    
    # Two-column layout for visualizations
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("#### 😴 Insomnia Severity Distribution")
        
        # ISI Categories
        def categorize_isi(score):
            if score < 8:
                return "No Insomnia (0-7)"
            elif score < 15:
                return "Subthreshold (8-14)"
            elif score < 22:
                return "Moderate (15-21)"
            else:
                return "Severe (22-28)"
        
        df['ISI_Category'] = df['InsomniaSeverity_index'].apply(categorize_isi)
        isi_counts = df['ISI_Category'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['#10b981', '#fbbf24', '#f97316', '#ef4444']
        isi_counts.plot(kind='bar', ax=ax, color=colors, edgecolor='black')
        ax.set_xlabel('Insomnia Severity', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Students', fontsize=12, fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        # Statistics
        st.info(f"""
        📊 **Key Insights:**
        - Average ISI Score: **{df['InsomniaSeverity_index'].mean():.1f}**
        - Median ISI Score: **{df['InsomniaSeverity_index'].median():.1f}**
        - Students needing intervention (ISI≥15): **{((df['InsomniaSeverity_index'] >= 15).sum() / len(df) * 100):.1f}%**
        """)
    
    with col_right:
        st.markdown("#### 🎯 Academic Performance Overview")
        
        # GPA Distribution
        gpa_order = ['Below 2.00', '2.00 - 2.49', '2.50 - 2.99', '3.00 - 3.49', '3.50 - 3.69', '3.70 - 4.00']
        gpa_counts = df['GPA'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_gpa = plt.cm.Blues([0.3, 0.4, 0.5, 0.6, 0.75, 0.9])
        
        # Reorder based on GPA ranges
        gpa_counts_ordered = gpa_counts.reindex([g for g in gpa_order if g in gpa_counts.index], fill_value=0)
        gpa_counts_ordered.plot(kind='bar', ax=ax, color=colors_gpa, edgecolor='black')
        ax.set_xlabel('GPA Range', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Students', fontsize=12, fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        # Academic performance stats
        excellent = df['AcademicPerformance'].str.contains('Excellent|Very good', na=False).sum()
        st.success(f"""
        🎓 **Academic Highlights:**
        - Students with GPA ≥ 3.50: **{df['GPA'].str.contains('3.50|3.70|4.00', na=False).sum()}**
        - Self-rated excellent/very good: **{excellent}** ({excellent/len(df)*100:.1f}%)
        - Average performance rating: **{df['AcademicPerformance'].mode()[0] if not df['AcademicPerformance'].mode().empty else 'N/A'}**
        """)
    
    st.markdown("---")
    
    # Demographics Overview
    st.markdown("#### 👥 Demographics & Faculty Distribution")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Gender Distribution**")
        gender_counts = df['Gender'].value_counts()
        for gender, count in gender_counts.items():
            pct = count / len(df) * 100
            st.metric(gender, f"{count}", f"{pct:.1f}%")
    
    with col2:
        st.markdown("**Year of Study**")
        year_counts = df['YearOfStudy'].value_counts().sort_index()
        for year, count in year_counts.items():
            pct = count / len(df) * 100
            st.write(f"**{year}**: {count} ({pct:.1f}%)")
    
    with col3:
        st.markdown("**Top Faculties**")
        faculty_counts = df['Faculty'].value_counts().head(3)
        for faculty, count in faculty_counts.items():
            faculty_short = faculty.split('(')[-1].replace(')', '') if '(' in faculty else faculty[:10]
            st.write(f"**{faculty_short}**: {count}")
    
    st.markdown("---")
    
    # Data Preview
    with st.expander("📋 View Raw Data", expanded=False):
        st.dataframe(
            df.head(50),
            use_container_width=True,
            hide_index=True
        )
        
        st.download_button(
            label="📥 Download Full Dataset (CSV)",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=f"umk_insomnia_data_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# Call render when this module is run
if __name__ == "__main__":
    render()
