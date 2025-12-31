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
    
    st.title("🏃 Lifestyle Factors Analysis")
    st.markdown("### Technology, Caffeine, Exercise, and Stress Impact on Sleep")
    st.markdown("---")
    
    # Key Lifestyle Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        devices = df['DeviceUsage'].str.contains('Always|Often', na=False).sum()
        st.metric("High Device Usage", f"{devices}",
                 f"{devices/len(df)*100:.1f}%",
                 delta_color="inverse",
                 help="Students using devices every night before sleep")
    
    with col2:
        caffeine = df['CaffeineConsumption'].str.contains('Always|Often', na=False).sum()
        st.metric("High Caffeine Users", f"{caffeine}",
                 f"{caffeine/len(df)*100:.1f}%",
                 delta_color="inverse")
    
    with col3:
        sedentary = df['PhysicalActivity'].str.contains('Never|Rarely', na=False).sum()
        st.metric("Sedentary Lifestyle", f"{sedentary}",
                 f"{sedentary/len(df)*100:.1f}%",
                 delta_color="inverse")
    
    with col4:
        high_stress = df['StressLevel'].str.contains('High|Very high', na=False).sum()
        st.metric("High Stress Levels", f"{high_stress}",
                 f"{high_stress/len(df)*100:.1f}%",
                 delta_color="inverse")
    
    st.markdown("---")
    
    # Technology & Sleep
    st.markdown("#### 📱 Technology Use Before Sleep")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        device_counts = df['DeviceUsage'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = plt.cm.Reds(np.linspace(0.3, 0.9, len(device_counts)))
        device_counts.plot(kind='barh', ax=ax, color=colors, edgecolor='black')
        ax.set_xlabel('Number of Students', fontsize=11, fontweight='bold')
        ax.set_ylabel('Device Usage Frequency', fontsize=11, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("**Device Impact:**")
        
        always_users = df['DeviceUsage'].str.contains('Always', na=False).sum()
        never_users = df['DeviceUsage'].str.contains('Never', na=False).sum()
        
        st.metric("Daily Users", always_users, f"{always_users/len(df)*100:.1f}%")
        st.metric("No Device Use", never_users, f"{never_users/len(df)*100:.1f}%")
        
        # Correlation with sleep quality
        device_users = df[df['DeviceUsage'].str.contains('Always|Often', na=False)]
        if len(device_users) > 0:
            avg_isi_devices = device_users['InsomniaSeverity_index'].mean()
            st.warning(f"""
            📱 **Blue Light Effect:**
            - Heavy device users have avg ISI: **{avg_isi_devices:.1f}**
            - Blue light suppresses melatonin production
            - Recommendation: Stop screen time 1hr before bed
            """)
    
    st.markdown("---")
    
    # Caffeine Consumption
    st.markdown("#### ☕ Caffeine Consumption Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        caffeine_counts = df['CaffeineConsumption'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_caffeine = ['#10b981', '#fbbf24', '#f97316', '#ef4444', '#dc2626']
        caffeine_counts.plot(kind='bar', ax=ax, 
                           color=colors_caffeine[:len(caffeine_counts)], 
                           edgecolor='black')
        ax.set_xlabel('Caffeine Consumption Frequency', fontsize=11, fontweight='bold')
        ax.set_ylabel('Number of Students', fontsize=11, fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("**Caffeine Stats:**")
        
        high_caffeine = df['CaffeineConsumption'].str.contains('Always|Often', na=False).sum()
        low_caffeine = df['CaffeineConsumption'].str.contains('Never|Rarely', na=False).sum()
        
        st.metric("High Consumers", high_caffeine, f"{high_caffeine/len(df)*100:.1f}%")
        st.metric("Low/No Caffeine", low_caffeine, f"{low_caffeine/len(df)*100:.1f}%")
        
        # Caffeine impact on sleep
        high_caff_users = df[df['CaffeineConsumption'].str.contains('Always|Often', na=False)]
        if len(high_caff_users) > 0:
            avg_isi_caff = high_caff_users['InsomniaSeverity_index'].mean()
            poor_sleep_caff = (high_caff_users['SleepQuality'].astype(str).isin(['1', '2'])).sum()
            
            st.info(f"""
            ☕ **Caffeine Impact:**
            - Avg ISI for high consumers: **{avg_isi_caff:.1f}**
            - Poor sleep quality: **{poor_sleep_caff}** students
            - Half-life: 5-6 hours (affects sleep if consumed late)
            """)
    
    st.markdown("---")
    
    # Physical Activity
    st.markdown("#### 🏃 Physical Activity & Exercise")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        activity_counts = df['PhysicalActivity'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_activity = plt.cm.Greens(np.linspace(0.3, 0.9, len(activity_counts)))
        activity_counts.plot(kind='barh', ax=ax, color=colors_activity, edgecolor='black')
        ax.set_xlabel('Number of Students', fontsize=11, fontweight='bold')
        ax.set_ylabel('Exercise Frequency', fontsize=11, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("**Activity Levels:**")
        
        active = df['PhysicalActivity'].str.contains('Always|Often|Sometimes', na=False).sum()
        sedentary = df['PhysicalActivity'].str.contains('Never|Rarely', na=False).sum()
        
        st.metric("Active Students", active, f"{active/len(df)*100:.1f}%")
        st.metric("Sedentary", sedentary, f"{sedentary/len(df)*100:.1f}%", 
                 delta_color="inverse")
        
        # Exercise benefits
        active_students = df[df['PhysicalActivity'].str.contains('Always|Often', na=False)]
        if len(active_students) > 0:
            avg_isi_active = active_students['InsomniaSeverity_index'].mean()
            good_sleep = (active_students['SleepQuality'].astype(str).isin(['4', '5'])).sum()
            
            st.success(f"""
            🏃 **Exercise Benefits:**
            - Avg ISI for active students: **{avg_isi_active:.1f}**
            - Good sleep quality: **{good_sleep}** students
            - Regular exercise improves sleep latency & quality
            """)
    
    st.markdown("---")
    
    # Stress Levels
    st.markdown("#### 😰 Academic Stress Levels")
    
    col1, col2 = st.columns(2)
    
    with col1:
        stress_counts = df['StressLevel'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        colors_stress = ['#10b981', '#3b82f6', '#fbbf24', '#f97316', '#ef4444']
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(stress_counts, labels=stress_counts.index,
                                           autopct='%1.1f%%',
                                           colors=colors_stress[:len(stress_counts)],
                                           startangle=90)
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title('Stress Level Distribution', fontsize=13, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("**Stress Impact:**")
        
        high_stress_count = df['StressLevel'].str.contains('High|Very high', na=False).sum()
        low_stress_count = df['StressLevel'].str.contains('Low|Very low', na=False).sum()
        
        st.metric("High Stress", high_stress_count, 
                 f"{high_stress_count/len(df)*100:.1f}%",
                 delta_color="inverse")
        st.metric("Low Stress", low_stress_count, 
                 f"{low_stress_count/len(df)*100:.1f}%")
        
        # Stress-sleep correlation
        high_stress_students = df[df['StressLevel'].str.contains('High|Very high', na=False)]
        if len(high_stress_students) > 0:
            avg_isi_stress = high_stress_students['InsomniaSeverity_index'].mean()
            poor_sleep_stress = (high_stress_students['SleepQuality'].astype(str).isin(['1', '2'])).sum()
            
            st.error(f"""
            😰 **Stress-Sleep Connection:**
            - Avg ISI for high-stress students: **{avg_isi_stress:.1f}**
            - Students with poor sleep: **{poor_sleep_stress}**
            - Stress is a major predictor of insomnia
            """)
    
    st.markdown("---")
    
    # Lifestyle Score Heatmap
    st.markdown("#### 🎯 Combined Lifestyle Risk Assessment")
    
    # Calculate lifestyle risk score
    def calculate_lifestyle_risk(row):
        risk = 0
        
        # Device usage risk
        if pd.notna(row['DeviceUsage']) and 'Always' in str(row['DeviceUsage']):
            risk += 3
        elif pd.notna(row['DeviceUsage']) and 'Often' in str(row['DeviceUsage']):
            risk += 2
        
        # Caffeine risk
        if pd.notna(row['CaffeineConsumption']) and 'Always' in str(row['CaffeineConsumption']):
            risk += 3
        elif pd.notna(row['CaffeineConsumption']) and 'Often' in str(row['CaffeineConsumption']):
            risk += 2
        
        # Exercise protective factor
        if pd.notna(row['PhysicalActivity']) and ('Never' in str(row['PhysicalActivity']) or 'Rarely' in str(row['PhysicalActivity'])):
            risk += 2
        
        # Stress risk
        if pd.notna(row['StressLevel']) and 'Very high' in str(row['StressLevel']):
            risk += 3
        elif pd.notna(row['StressLevel']) and 'High' in str(row['StressLevel']):
            risk += 2
        
        return risk
    
    df['Lifestyle_Risk'] = df.apply(calculate_lifestyle_risk, axis=1)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        low_risk = (df['Lifestyle_Risk'] <= 3).sum()
        st.metric("Low Risk", low_risk, f"{low_risk/len(df)*100:.1f}%")
    
    with col2:
        moderate_risk = ((df['Lifestyle_Risk'] > 3) & (df['Lifestyle_Risk'] <= 6)).sum()
        st.metric("Moderate Risk", moderate_risk, f"{moderate_risk/len(df)*100:.1f}%")
    
    with col3:
        high_risk = (df['Lifestyle_Risk'] > 6).sum()
        st.metric("High Risk", high_risk, f"{high_risk/len(df)*100:.1f}%",
                 delta_color="inverse")
    
    # Distribution of lifestyle risk
    fig, ax = plt.subplots(figsize=(10, 5))
    df['Lifestyle_Risk'].hist(bins=12, ax=ax, color='#6366f1', edgecolor='black')
    ax.set_xlabel('Lifestyle Risk Score (0-11)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Number of Students', fontsize=11, fontweight='bold')
    ax.set_title('Distribution of Lifestyle Risk Factors', fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.info("""
    📊 **Lifestyle Risk Score Calculation:**
    - Device usage before bed: +2-3 points
    - High caffeine consumption: +2-3 points
    - Lack of exercise: +2 points
    - High stress levels: +2-3 points
    
    **Interpretation:**
    - 0-3: Low risk (good sleep hygiene practices)
    - 4-6: Moderate risk (some lifestyle improvements needed)
    - 7+: High risk (multiple factors affecting sleep quality)
    """)
    
    st.markdown("---")
    
    # Recommendations
    with st.expander("💡 Lifestyle Modification Recommendations", expanded=True):
        st.markdown("""
        ### Personalized Lifestyle Changes:
        
        #### 📱 Technology Management:
        - **Digital Sunset**: Stop all screens 1-2 hours before bed
        - **Blue Light Filters**: Use night mode/blue light blocking glasses
        - **Bedroom Rules**: Keep phones out of the bedroom
        - **Alternative Activities**: Read physical books, journal, meditate
        
        #### ☕ Caffeine Strategy:
        - **Timing**: No caffeine after 2 PM
        - **Alternatives**: Switch to herbal tea in afternoon/evening
        - **Gradual Reduction**: Slowly decrease if heavily dependent
        - **Hydration**: Replace with water for energy
        
        #### 🏃 Exercise Integration:
        - **Morning/Afternoon**: Best times for vigorous exercise
        - **Consistency**: Even 20-30 minutes daily helps
        - **Evening Options**: Gentle yoga or stretching before bed
        - **Outdoor Time**: Natural light exposure helps circadian rhythm
        
        #### 😌 Stress Management:
        - **Mindfulness**: Daily meditation or breathing exercises
        - **Time Management**: Better planning reduces last-minute stress
        - **Support Systems**: Talk to friends, family, or counselors
        - **Boundaries**: Learn to say no and prioritize self-care
        
        ### 🎯 Quick Wins (Start Today):
        1. Set a phone alarm to stop screen time at 9 PM
        2. Take a 15-minute walk tomorrow afternoon
        3. Practice 5 minutes of deep breathing before bed
        4. Schedule your last coffee by 2 PM
        """)

if __name__ == "__main__":
    render()
