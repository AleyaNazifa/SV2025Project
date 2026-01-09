import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from data_loader import display_sidebar_info, get_df
from cleaning_aelyana import prepare_aelyana_data

# -------------------------------------------------
# Utility
# -------------------------------------------------
def safe_mode(s, default="N/A"):
    s = s.dropna()
    return s.mode().iloc[0] if not s.empty else default


# -------------------------------------------------
# MAIN RENDER FUNCTION
# -------------------------------------------------
def render():
    display_sidebar_info()

    raw = get_df()
    df = prepare_aelyana_data(raw)

    if df is None or df.empty:
        st.error("No data available.")
        return

    # -----------------------------
    # CATEGORY ORDERS
    # -----------------------------
    academic_order = ['Below average', 'Average', 'Good', 'Very good', 'Excellent']
    insomnia_order = ['Low / No Insomnia', 'Moderate Insomnia', 'Severe Insomnia']
    freq_order = ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']
    impact_order = ['No impact', 'Minor impact', 'Moderate impact', 'Major impact', 'Severe impact']

    # Convert to categorical (order-safe)
    df['AcademicPerformance'] = pd.Categorical(df['AcademicPerformance'], categories=academic_order, ordered=True)
    df['Insomnia_Category'] = pd.Categorical(df['Insomnia_Category'], categories=insomnia_order, ordered=True)
    df['ConcentrationDifficulty'] = pd.Categorical(df['ConcentrationDifficulty'], categories=freq_order, ordered=True)
    df['AssignmentImpact'] = pd.Categorical(df['AssignmentImpact'], categories=impact_order, ordered=True)
    df['DaytimeFatigue'] = pd.Categorical(df['DaytimeFatigue'], categories=freq_order, ordered=True)

    # -----------------------------
    # HEADER
    # -----------------------------
    st.title("Interpretation Dashboard: Impact of Sleep Related Issues on Academic Performance")

    # =============================
    # 🔹 KEY METRICS
    # =============================
    st.subheader("Key Findings: The Impact of Insomnia")
    col1, col2, col3, col4 = st.columns(4)

    severe = df[df['Insomnia_Category'] == 'Severe Insomnia']

    focus_risk = severe['ConcentrationDifficulty'].isin(['Often', 'Always']).mean() * 100
    fatigue_risk = severe['DaytimeFatigue'].isin(['Often', 'Always']).mean() * 100
    perf_level = safe_mode(severe['AcademicPerformance'])
    assign_risk = severe['AssignmentImpact'].isin(['Major impact', 'Severe impact']).mean() * 100

    col1.metric("🧠 Concentration Difficulty", f"{focus_risk:.1f}%")
    col2.metric("😫 Severe Academic Fatigue", f"{fatigue_risk:.1f}%")
    col3.metric("📉 Academic Performance Level", perf_level)
    col4.metric("📝 Assignment Performance Risk", f"{assign_risk:.1f}%")

    st.divider()

    # =============================
    # CHART 1: Concentration
    # =============================
    tab = pd.crosstab(df['Insomnia_Category'], df['ConcentrationDifficulty'], dropna=False)
    melted = tab.reset_index().melt(id_vars='Insomnia_Category', value_name='Count')

    fig = px.bar(
        melted, x='Insomnia_Category', y='Count', color='ConcentrationDifficulty',
        barmode='group',
        title='Concentration Difficulty by Insomnia Category',
        category_orders={"Insomnia_Category": insomnia_order, "ConcentrationDifficulty": freq_order}
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**  
There is a clear escalation in concentration difficulty as insomnia severity increases, indicating a strong cognitive impact of poor sleep.
""")
    st.divider()

    # =============================
    # CHART 2: GPA vs Insomnia Index
    # =============================
    fig = px.box(
        df, x='GPA', y='InsomniaSeverity_index', color='GPA',
        title='Insomnia Severity Index Across GPA Categories',
        points='outliers'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.divider()

    # =============================
    # CHART 3: Assignment Impact
    # =============================
    tab = pd.crosstab(df['Insomnia_Category'], df['AssignmentImpact'], dropna=False)
    melted = tab.reset_index().melt(id_vars='Insomnia_Category', value_name='Student_Count')

    fig = px.bar(
        melted, x='Insomnia_Category', y='Student_Count', color='AssignmentImpact',
        barmode='stack',
        title='Assignment Impact by Insomnia Category',
        category_orders={"AssignmentImpact": impact_order}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.divider()

    # =============================
    # CHART 4: Daytime Fatigue
    # =============================
    tab = pd.crosstab(df['Insomnia_Category'], df['DaytimeFatigue'], dropna=False)
    melted = tab.reset_index().melt(id_vars='Insomnia_Category', value_name='Count')

    fig = px.bar(
        melted, x='Insomnia_Category', y='Count', color='DaytimeFatigue',
        barmode='stack',
        title='Fatigue Level by Insomnia Severity',
        category_orders={"DaytimeFatigue": freq_order}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.divider()

    # =============================
    # CHART 5: Academic Performance
    # =============================
    fig = px.box(
        df, x='Insomnia_Category', y='AcademicPerformance',
        title='Academic Performance by Insomnia Severity',
        category_orders={"AcademicPerformance": academic_order},
        points='outliers'
    )
    fig.update_layout(yaxis=dict(autorange='reversed'))
    st.plotly_chart(fig, use_container_width=True)
    st.divider()

    # =============================
    # CHART 6: Correlation Heatmap
    # =============================
    corr_cols = [
        'SleepHours_est', 'InsomniaSeverity_index', 'DaytimeFatigue_numeric',
        'ConcentrationDifficulty_numeric', 'MissedClasses_numeric',
        'AcademicPerformance_numeric', 'GPA_numeric', 'CGPA_numeric'
    ]
    corr_cols = [c for c in corr_cols if c in df.columns]

    corr = df[corr_cols].corr()
    fig = px.imshow(corr, text_auto=".2f", aspect="auto",
                    title="Correlation Heatmap: Sleep Issues vs Academic Outcomes")
    st.plotly_chart(fig, use_container_width=True)


# -------------------------------------------------
# ENTRY POINT
# -------------------------------------------------
render()
