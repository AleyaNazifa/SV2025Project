import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import display_sidebar_info, get_df
from cleaning_aelyana import prepare_aelyana_data


def render():
    # ==========================================
    # 1. SIDEBAR & DATA LOADING
    # ==========================================
    display_sidebar_info()

    raw = get_df()
    df = prepare_aelyana_data(raw)

    if df is None or df.empty:
        st.error("No data available.")
        return

    # ==========================================
    # 2. CATEGORY ORDERS
    # ==========================================
    academic_order = ["Below average", "Average", "Good", "Very good", "Excellent"]
    insomnia_order = ["Low / No Insomnia", "Moderate Insomnia", "Severe Insomnia"]
    freq_order = ["Never", "Rarely", "Sometimes", "Often", "Always"]
    impact_order = ["No impact", "Minor impact", "Moderate impact", "Major impact", "Severe impact"]

    # ==========================================
    # 3. TYPE CONVERSION
    # ==========================================
    df['AcademicPerformance'] = pd.Categorical(
        df['AcademicPerformance'], categories=academic_order, ordered=True
    )
    df['Insomnia_Category'] = pd.Categorical(
        df['Insomnia_Category'], categories=insomnia_order, ordered=True
    )
    df['ConcentrationDifficulty'] = pd.Categorical(
        df['ConcentrationDifficulty'], categories=freq_order, ordered=True
    )
    df['AssignmentImpact'] = pd.Categorical(
        df['AssignmentImpact'], categories=impact_order, ordered=True
    )
    df['DaytimeFatigue'] = pd.Categorical(
        df['DaytimeFatigue'], categories=freq_order, ordered=True
    )

    # ==========================================
    # 4. DASHBOARD HEADER
    # ==========================================
    st.title("Interpretation Dashboard: Impact of Sleep Related Issues on Academic Performance")
    st.markdown("### How sleep-related issues affect focus, fatigue, assignments, and performance")
    st.divider()

    # ==========================================
    # 5. KEY METRICS (OBJECTIVE-DRIVEN)
    # ==========================================
    st.subheader("Key Findings: The Impact of Severe Insomnia")

    col1, col2, col3, col4 = st.columns(4)

    severe_insomnia_df = df[df['Insomnia_Category'] == 'Severe Insomnia']

    focus_risk = (severe_insomnia_df['ConcentrationDifficulty']
                  .isin(['Often', 'Always']).mean() * 100)

    fatigue_impact = (severe_insomnia_df['DaytimeFatigue']
                      .isin(['Often', 'Always']).mean() * 100)

    perf_impact = (
        severe_insomnia_df['AcademicPerformance'].mode()[0]
        if not severe_insomnia_df.empty else "N/A"
    )

    assign_impact = (severe_insomnia_df['AssignmentImpact']
                     .isin(['Major impact', 'Severe impact']).mean() * 100)

    col1.metric(
        "🧠 Concentration Difficulty",
        f"{focus_risk:.1f}%",
        help="Students with severe insomnia who often/always struggle to concentrate"
        border=True
    )

    col2.metric(
        "😫 Daytime Fatigue",
        f"{fatigue_impact:.1f}%",
        help="Students with severe insomnia who frequently feel fatigued"
        border=True
    )

    col3.metric(
        "📉 Academic Performance",
        perf_impact,
        help="Most common academic performance level for severe insomnia group"
        border=True
    )

    col4.metric(
        "📝 Assignment Impact",
        f"{assign_impact:.1f}%",
        help="Students reporting major or severe assignment difficulties"
        border=True
    )

    st.divider()

    # ==========================================
    # 6. VISUALIZATION 1: CONCENTRATION DIFFICULTY
    # ==========================================
    concentration_table = pd.crosstab(
        df['Insomnia_Category'], df['ConcentrationDifficulty'], dropna=False
    )

    concentration_melted = concentration_table.reset_index().melt(
        id_vars='Insomnia_Category',
        var_name='ConcentrationDifficulty',
        value_name='Count'
    )

    fig1 = px.bar(
        concentration_melted,
        x='Insomnia_Category',
        y='Count',
        color='ConcentrationDifficulty',
        barmode='group',
        title='Concentration Difficulty by Insomnia Category',
        category_orders={
            "ConcentrationDifficulty": freq_order,
            "Insomnia_Category": insomnia_order
        },
        color_discrete_sequence=px.colors.sequential.Sunset
    )

    st.plotly_chart(fig1, use_container_width=True)
    st.divider()

    # ==========================================
    # 7. VISUALIZATION 2: GPA vs INSOMNIA (BOX)
    # ==========================================
    fig2 = px.box(
        df,
        x="GPA",
        y="InsomniaSeverity_index",
        color="GPA",
        title="Insomnia Severity Index Across GPA Categories",
        color_discrete_sequence=px.colors.sequential.Sunset,
        points="outliers"
    )

    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
    st.divider()

    # ==========================================
    # 8. VISUALIZATION 3: ASSIGNMENT IMPACT
    # ==========================================
    assignment_table = pd.crosstab(
        df['Insomnia_Category'], df['AssignmentImpact'], dropna=False
    )

    assignment_melted = assignment_table.reset_index().melt(
        id_vars='Insomnia_Category',
        var_name='AssignmentImpact',
        value_name='Count'
    )

    fig3 = px.bar(
        assignment_melted,
        x='Insomnia_Category',
        y='Count',
        color='AssignmentImpact',
        barmode='stack',
        title="Assignment Impact by Insomnia Category",
        category_orders={
            "AssignmentImpact": impact_order,
            "Insomnia_Category": insomnia_order
        },
        color_discrete_sequence=px.colors.sequential.Sunset
    )

    st.plotly_chart(fig3, use_container_width=True)
    st.divider()

    # ==========================================
    # 9. VISUALIZATION 4: DAYTIME FATIGUE
    # ==========================================
    fatigue_table = pd.crosstab(
        df['Insomnia_Category'], df['DaytimeFatigue'], dropna=False
    )

    fatigue_melted = fatigue_table.reset_index().melt(
        id_vars='Insomnia_Category',
        var_name='DaytimeFatigue',
        value_name='Count'
    )

    fig4 = px.bar(
        fatigue_melted,
        x='Insomnia_Category',
        y='Count',
        color='DaytimeFatigue',
        barmode='stack',
        title="Daytime Fatigue by Insomnia Severity",
        category_orders={
            "DaytimeFatigue": freq_order,
            "Insomnia_Category": insomnia_order
        },
        color_discrete_sequence=px.colors.sequential.Sunset
    )

    st.plotly_chart(fig4, use_container_width=True)
    st.divider()

    # ==========================================
    # 10. VISUALIZATION 5: CORRELATION HEATMAP
    # ==========================================
    corr_cols = [
        'SleepHours_est',
        'InsomniaSeverity_index',
        'DaytimeFatigue_numeric',
        'ConcentrationDifficulty_numeric',
        'MissedClasses_numeric',
        'AcademicPerformance_numeric',
        'GPA_numeric',
        'CGPA_numeric'
    ]

    corr_cols = [c for c in corr_cols if c in df.columns]
    corr_matrix = df[corr_cols].corr()

    fig5 = px.imshow(
        corr_matrix,
        text_auto=".2f",
        aspect="auto",
        title="Correlation Heatmap: Sleep Issues vs Academic Outcomes",
        color_continuous_scale="Sunset"
    )

    st.plotly_chart(fig5, use_container_width=True)


# ==========================================
# STREAMLIT PAGE ENTRY POINT
# ==========================================
render()
