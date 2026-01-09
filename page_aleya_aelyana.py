import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Interpretation Dashboard: Impact of Sleep Related Issues on Academic Performance", 
    layout="wide"
)

# ==========================================
# 2. DATA LOADING & PRE-PROCESSING
# ==========================================
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/aleya566/project/refs/heads/main/final_processed_data%20(8).csv'
    df = pd.read_csv(url)
    
    # Define category orders (Used across all charts)
    academic_order = ['Below average', 'Average', 'Good', 'Very good', 'Excellent']
    insomnia_order = ['Low / No Insomnia', 'Moderate Insomnia', 'Severe Insomnia']
    freq_order = ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']
    impact_order = ['No impact', 'Minor impact', 'Moderate impact', 'Major impact', 'Severe impact']
    
    # Convert columns to categorical type to ensure correct ordering in plots
    df['AcademicPerformance'] = pd.Categorical(df['AcademicPerformance'], categories=academic_order, ordered=True)
    df['Insomnia_Category'] = pd.Categorical(df['Insomnia_Category'], categories=insomnia_order, ordered=True)
    df['ConcentrationDifficulty'] = pd.Categorical(df['ConcentrationDifficulty'], categories=freq_order, ordered=True)
    df['AssignmentImpact'] = pd.Categorical(df['AssignmentImpact'], categories=impact_order, ordered=True)
    df['DaytimeFatigue'] = pd.Categorical(df['DaytimeFatigue'], categories=freq_order, ordered=True)
    
    return df, academic_order, insomnia_order, freq_order, impact_order

df, academic_order, insomnia_order, freq_order, impact_order = load_data()

# ==========================================
# 3. DASHBOARD HEADER
# ==========================================
st.title("Interpretation Dashboard: Impact of Sleep Related Issues on Academic Performance")

# ==============================================
# 🔹 KEY METRICS SECTION (Objective-Driven)
# ==============================================
st.subheader("Key Findings: The Impact of Insomnia")
col1, col2, col3, col4 = st.columns(4)

# Filtering data to isolate the high-impact group for metrics
severe_insomnia_df = df[df['Insomnia_Category'] == 'Severe Insomnia']

# A. Focus Risk (Concentration Difficulty)
focus_risk = (severe_insomnia_df['ConcentrationDifficulty'].isin(['Often', 'Always']).mean() * 100)

# B. Fatigue Impact (Daytime Fatigue)
fatigue_impact = (severe_insomnia_df['DaytimeFatigue'].isin(['Often', 'Always']).mean() * 100)

# C. Performance Trend (Most common performance for Severe group)
perf_impact = severe_insomnia_df['AcademicPerformance'].mode()[0] if not severe_insomnia_df.empty else "N/A"

# D. Assignment Risk (Percentage reporting Major/Severe impact)
assign_impact = (severe_insomnia_df['AssignmentImpact'].isin(['Major impact', 'Severe impact']).mean() * 100)

# Display key academic impact metrics
col1.metric(
    label="🧠 Concentration Difficulty",
    value=f"{focus_risk:.1f}%",
    help="Percentage of students with severe insomnia who report frequent difficulty concentrating",
    border=True
)

col2.metric(
    label="😫 Severe Academic Fatigue",
    value=f"{fatigue_impact:.1f}%",
    help="Percentage of students with severe insomnia experiencing frequent daytime fatigue",
    border=True
)

col3.metric(
    label="📉 Academic Performance Level",
    value=perf_impact,
    help="Most frequently reported academic performance category among students with severe insomnia",
    border=True
)

col4.metric(
    label="📝 Assignment Performance Risk",
    value=f"{assign_impact:.1f}%",
    help="Percentage of students with severe insomnia reporting major or severe difficulty completing assignments",
    border=True
)

st.divider()

# ==========================================
# 4. VISUALIZATIONS (ORIGINAL LAYOUT)
# ==========================================

# --- CHART 1: Concentration Difficulty (Grouped Bar) ---
concentration_crosstab = pd.crosstab(df['Insomnia_Category'], df['ConcentrationDifficulty'], dropna=False)
concentration_melted = concentration_crosstab.reset_index().melt(id_vars='Insomnia_Category', var_name='ConcentrationDifficulty', value_name='Count')

fig2 = px.bar(
    concentration_melted, x='Insomnia_Category', y='Count', color='ConcentrationDifficulty',
    barmode='group', title='Concentration Difficulty by Insomnia Category',
    category_orders={"ConcentrationDifficulty": freq_order, "Insomnia_Category": insomnia_order},
    color_discrete_sequence=px.colors.sequential.Sunset,
    labels={'Count': 'Number of Students', 'Insomnia_Category': 'Insomnia Level'}
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
**Key Insights**
* Most students (64) have moderate insomnia, with "Sometimes" (36 students) being the most common focus problem.
* Low / No Insomnia Group dominated by "Rarely" (9) and "Sometimes" (8) responses, serious disruptions ("Often"/"Always") are almost none.
* Severe Insomnia Group shows a concerning change which "Rarely" almost disappears (1 student), replaced by a sharp increase in "Often" and "Always".
* Zero (0) students reported "Never" experiencing concentration issues, proving that focus is a universal challenge, but it becomes chronic with poor sleep.

**Conclusion**
* There is a direct relationship between insomnia severity and difficulty maintaining focus. Severe insomnia doesn't just mean less sleep but it creates a high risk of academic failure due to ongoing cognitive impairment.
""")
st.divider()

# --- CHART 2: GPA vs Insomnia Index (Box Plot) ---
gpa_order = sorted(df['GPA'].unique()) 
fig3 = px.box(
    df, x="GPA", y="InsomniaSeverity_index", color="GPA",
    title="Insomnia Severity Index Across GPA Categories",
    category_orders={"GPA": gpa_order},
    color_discrete_sequence=px.colors.sequential.Sunset,
    points="outliers"
)
fig3.update_layout(xaxis_title="GPA Category", yaxis_title="Insomnia Severity Index", showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
**Key Insights**
* As GPA decreases, the insomnia severity "box" shifts upward. Higher GPA is associated with more consistent and lower insomnia scores.
* GPA 3.70 - 4.00 category show lowest median insomnia score (4), placing these students in the "Low/No Insomnia" category.
* GPA 3.00 - 3.69 category show median score increases to 7. Interestingly, outliers reaching scores of 12-13 indicate that some students maintain good grades despite high insomnia.
* GPA 2.50 - 2.49 group show highest spread and maximum scores (reaching 14), indicating that this group experiences the strongest insomnia symptoms.

**Conclusion**
* Managing insomnia is a key factor in academic success. Students with the best grades tend to maintain the healthiest sleep profiles.
""")
st.divider()

# --- CHART 3: Assignment Impact (Stacked Bar) ---
assignment_table = pd.crosstab(df["Insomnia_Category"], df["AssignmentImpact"], dropna=False)
assignment_melted = assignment_table.reset_index().melt(id_vars='Insomnia_Category', var_name='AssignmentImpact', value_name='Student_Count')

fig4 = px.bar(
    assignment_melted, x='Insomnia_Category', y='Student_Count', color='AssignmentImpact',
    title="Assignment Impact by Insomnia Category",
    category_orders={"AssignmentImpact": impact_order, "Insomnia_Category": insomnia_order},
    color_discrete_sequence=px.colors.sequential.Sunset,
    labels={'Student_Count': 'Number of Students'}
)
fig4.update_layout(barmode='stack', xaxis_title="Insomnia Category", yaxis_title="Number of Students")
st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
**Key Insights**
* Low / No Insomnia: Even with good sleep, only 3 students reported "No impact," with most feeling at least a "Minor impact" (8) on their work.
* Moderate Insomnia: A large spike in "Moderate" (28) and "Major" (13) impacts, indicating that sleep issues are starting to damage the quality of their assignment.
* Severe Insomnia: Negative impact is the standard.16 out of 21 students are "Moderate" or "Major" impacted, with only 1 student reporting "No impact".

**Conclusion**
* The insomnia severity is directly correlates with academic disruption. As sleep health worsens, the ability to complete coursework effectively is significantly compromised.
""")
st.divider()

# --- CHART 4: Daytime Fatigue (Stacked Bar) ---
fatigue_table = pd.crosstab(df['Insomnia_Category'], df['DaytimeFatigue'], dropna=False)
fatigue_melted = fatigue_table.reset_index().melt(id_vars='Insomnia_Category', var_name='DaytimeFatigue', value_name='Count')

fig5 = px.bar(
    fatigue_melted, x='Insomnia_Category', y='Count', color='DaytimeFatigue',
    title="Fatigue Level by Insomnia Severity",
    category_orders={"DaytimeFatigue": freq_order, "Insomnia_Category": insomnia_order},
    color_discrete_sequence=px.colors.sequential.Sunset,
    barmode='stack'
)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("""
**Key Insights**
* Low / No Insomnia: Most students feel energized, with "Rarely" (11) or "Never" (4) being the top responses.
* Moderate Insomnia: A big shift where "Sometimes" (37) becomes the norm. The appearance of "Always" fatigued students (3) shows moderate issues can still cause persistent fatigue.
* Severe Insomnia: Fatigue is nearly universal. 20 out of 21 students reported fatigue "Sometimes" to "Always".

**Conclusion**
* There is a progressive increase in fatigue associated with sleep health. Fatigue acts as a barrier that may drive the concentration and performance issues seen throughout this study.
""")
st.divider()

# --- CHART 5: Academic Performance (Box Plot) ---
fig6 = px.box(
    df, x='Insomnia_Category', y='AcademicPerformance', color='Insomnia_Category',
    title="Academic Performance by Insomnia Severity",
    category_orders={"AcademicPerformance": academic_order, "Insomnia_Category": insomnia_order},
    color_discrete_sequence=px.colors.sequential.Sunset,
    points="outliers" 
)
fig6.update_layout(xaxis_title="Insomnia Severity", yaxis_title="Academic Performance (GPA / Self-rated)", showlegend=False, yaxis=dict(autorange="reversed"))
st.plotly_chart(fig6, use_container_width=True)

st.markdown("""
**Key Insights**
* Low/No Insomnia students feel the most confident, rating themselves between "Good" and "Very good".
* Moderate Insomnia causes ratings to spread out. The median remains "Good," but the range drops to "Average".
* Severe Insomnia shifts the entire box down to "Average" and "Good," with almost no representation of "Very good".

**Conclusion**
* Insomnia severity has a negative correlation with academic self perception. Severe insomnia acts as a "ceiling" that makes it harder to achieve or feel like a high achiever.
""")
st.divider()

# --- CHART 6: Correlation Heatmap ---
corr_columns = ['SleepHours_est', 'InsomniaSeverity_index', 'DaytimeFatigue_numeric', 'ConcentrationDifficulty_numeric', 'MissedClasses_numeric', 'AcademicPerformance_numeric', 'GPA_numeric', 'CGPA_numeric']
existing_cols = [c for c in corr_columns if c in df.columns]
corr_matrix = df[existing_cols].corr()

fig7 = px.imshow(
    corr_matrix, text_auto=".2f", aspect="auto",
    color_continuous_scale='Sunset',
    title="Correlation Heatmap: Sleep Issues vs. Academic Outcomes"
)
st.plotly_chart(fig7, use_container_width=True)

st.markdown("""
**Key Insights**
* Sleep hours is moderately correlated with Academic Performance (0.32), but much weaker correlated with actual GPA (0.16) and CGPA (-0.02).
* Fatigue and Concentration are strongly correlated (0.63). Insomnia Severity is also strongly correlated with Fatigue (0.54) and Concentration (0.38).
* Skipping classes is more damaging to long-term grades (-0.14) than the feeling of being tired alone.
* The small positive correlation (0.14) between sleep hours and fatigue suggests that getting more sleep doesn't always solve the problem.

**Conclusion**
* While sleep health determines student experience (fatigue/focus), its relationship to actual grades is complex. Success is more threatened by behavioral consequences (missing class) than just feeling tired.
""")
