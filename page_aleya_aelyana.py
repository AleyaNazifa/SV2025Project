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
    
    st.title("😴 Sleep Patterns Analysis")
    st.markdown("### Deep Dive into Student Sleep Behaviors and Quality")
    st.markdown("---")
    
    # Key Sleep Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_sleep = df['SleepHours'].str.extract(r'(\d+)').astype(float).mean().values[0]
        st.metric("Avg Sleep Duration", f"{avg_sleep:.1f}h", 
                 delta=f"{avg_sleep - 7:.1f}h vs ideal")
    
    with col2:
        poor_quality = (df['SleepQuality'].astype(str).isin(['1', '2'])).sum()
        st.metric("Poor Sleep Quality", f"{poor_quality}", 
                 f"{poor_quality/len(df)*100:.1f}%",
                 delta_color="inverse")
    
    with col3:
        late_sleepers = df['BedTime'].str.contains('12 AM|1 AM|2 AM', na=False).sum()
        st.metric("Late Sleepers (≥12 AM)", f"{late_sleepers}",
                 f"{late_sleepers/len(df)*100:.1f}%",
                 delta_color="inverse")
    
    with col4:
        frequent_wakeups = df['NightWakeups'].str.contains('Often|Always', na=False).sum()
        st.metric("Frequent Night Wakeups", f"{frequent_wakeups}",
                 f"{frequent_wakeups/len(df)*100:.1f}%",
                 delta_color="inverse")
    
    st.markdown("---")
    
    # Two-column layout
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("#### 🛏️ Sleep Duration Distribution")
        
        sleep_order = ['Less than 4 hours', '4–5 hours', '5–6 hours', '7–8 hours', '9 or more hours']
        sleep_counts = df['SleepHours'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['#ef4444', '#f97316', '#fbbf24', '#10b981', '#3b82f6']
        
        sleep_counts_ordered = sleep_counts.reindex([s for s in sleep_order if s in sleep_counts.index], fill_value=0)
        sleep_counts_ordered.plot(kind='barh', ax=ax, color=colors, edgecolor='black')
        ax.set_xlabel('Number of Students', fontsize=11, fontweight='bold')
        ax.set_ylabel('Sleep Duration', fontsize=11, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        # Sleep recommendations
        adequate = df['SleepHours'].str.contains('7–8|9 or more', na=False).sum()
        st.info(f"""
        💤 **Sleep Duration Insights:**
        - Students with adequate sleep (≥7h): **{adequate}** ({adequate/len(df)*100:.1f}%)
        - Sleep-deprived (<6h): **{len(df) - adequate}** ({(len(df)-adequate)/len(df)*100:.1f}%)
        - Recommendation: 7-9 hours for optimal cognitive function
        """)
    
    with col_right:
        st.markdown("#### ⭐ Sleep Quality Ratings")
        
        quality_counts = df['SleepQuality'].astype(str).value_counts().sort_index()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_quality = plt.cm.RdYlGn(np.linspace(0.2, 0.9, len(quality_counts)))
        
        quality_counts.plot(kind='bar', ax=ax, color=colors_quality, edgecolor='black')
        ax.set_xlabel('Sleep Quality Rating (1=Poor, 5=Excellent)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Number of Students', fontsize=11, fontweight='bold')
        ax.set_xticklabels([f"Rating {x}" for x in quality_counts.index], rotation=0)
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        avg_quality = df['SleepQuality'].astype(float).mean()
        good_quality = df['SleepQuality'].astype(str).isin(['4', '5']).sum()
        st.success(f"""
        ⭐ **Sleep Quality Summary:**
        - Average rating: **{avg_quality:.2f}/5.0**
        - Good/Excellent quality (4-5): **{good_quality}** ({good_quality/len(df)*100:.1f}%)
        - Students needing intervention: **{(df['SleepQuality'].astype(str).isin(['1', '2'])).sum()}**
        """)
    
    st.markdown("---")
    
    # Bedtime Analysis
    st.markdown("#### 🌙 Bedtime Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        bedtime_counts = df['BedTime'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        bedtime_counts.plot(kind='bar', ax=ax, color='#6366f1', edgecolor='black')
        ax.set_xlabel('Bedtime', fontsize=11, fontweight='bold')
        ax.set_ylabel('Number of Students', fontsize=11, fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("**Bedtime Categories:**")
        
        early = df['BedTime'].str.contains('9–10 PM|10–11 PM', na=False).sum()
        moderate = df['BedTime'].str.contains('11 PM–12 AM', na=False).sum()
        late = df['BedTime'].str.contains('After 12 AM', na=False).sum()
        
        st.metric("Early (Before 11 PM)", early, f"{early/len(df)*100:.1f}%")
        st.metric("Moderate (11 PM - 12 AM)", moderate, f"{moderate/len(df)*100:.1f}%")
        st.metric("Late (After 12 AM)", late, f"{late/len(df)*100:.1f}%", delta_color="inverse")
        
        st.warning(f"⚠️ **{late/len(df)*100:.1f}%** of students have delayed sleep schedules, which may impact circadian rhythm and academic performance.")
    
    st.markdown("---")
    
    # Sleep Difficulties
    st.markdown("#### 🚨 Sleep Difficulties & Disturbances")
    
    tab1, tab2, tab3 = st.tabs(["Falling Asleep", "Night Wakeups", "Daytime Napping"])
    
    with tab1:
        difficulty_counts = df['DifficultyFallingAsleep'].value_counts()
        
        col1, col2 = st.columns([2, 1])
        with col1:
            fig, ax = plt.subplots(figsize=(8, 4))
            difficulty_counts.plot(kind='barh', ax=ax, color='#f59e0b', edgecolor='black')
            ax.set_xlabel('Number of Students', fontsize=11, fontweight='bold')
            ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            chronic = df['DifficultyFallingAsleep'].str.contains('Often|Always', na=False).sum()
            st.metric("Chronic Difficulty", chronic, f"{chronic/len(df)*100:.1f}%", delta_color="inverse")
            
            st.info(f"**{chronic}** students experience frequent difficulty falling asleep, indicating potential insomnia.")
    
    with tab2:
        wakeup_counts = df['NightWakeups'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 4))
        wakeup_counts.plot(kind='bar', ax=ax, color='#8b5cf6', edgecolor='black')
        ax.set_xlabel('Frequency of Night Wakeups', fontsize=11, fontweight='bold')
        ax.set_ylabel('Number of Students', fontsize=11, fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        frequent = df['NightWakeups'].str.contains('Often|Always', na=False).sum()
        st.warning(f"⚠️ **{frequent}** students ({frequent/len(df)*100:.1f}%) experience frequent night wakeups, affecting sleep continuity.")
    
    with tab3:
        nap_counts = df['DayNap'].value_counts()
        
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(6, 6))
            nap_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', 
                           colors=['#10b981', '#fbbf24', '#ef4444'],
                           startangle=90)
            ax.set_ylabel('')
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.markdown("**Napping Patterns:**")
            for nap_type, count in nap_counts.items():
                st.write(f"**{nap_type}**: {count} students")
            
            regular_nappers = df['DayNap'].str.contains('Yes', na=False).sum()
            st.info(f"""
            💤 **Napping Insight:**
            - Regular nappers: **{regular_nappers}** ({regular_nappers/len(df)*100:.1f}%)
            - May indicate sleep debt or fatigue compensation
            """)
    
    st.markdown("---")
    
    # Sleep Methods
    with st.expander("💡 Sleep Methods Used by Students", expanded=True):
        st.markdown("**Methods students use to help them sleep:**")
        
        methods = df['SleepMethods'].dropna().value_counts().head(10)
        
        if len(methods) > 0:
            for method, count in methods.items():
                st.write(f"- **{method}** ({count} students)")
        else:
            st.info("Not enough data on sleep methods.")

if __name__ == "__main__":
    render()
