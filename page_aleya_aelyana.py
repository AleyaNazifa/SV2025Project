import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import display_sidebar_info, get_df
from cleaning_aelyana import prepare_aelyana_data


def render():
    # ==========================================
    # 1. SIDEBAR & DATA
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
    df['AcademicPerformance'] = pd.Categorical(df['AcademicPerformance'], categories=academic_order, ordered=True)
    df['Insomnia_Category'] = pd.Categorical(df['Insomnia_Category'], categories=insomnia_order, ordered=True)
    df['ConcentrationDifficulty'] = pd.Categorical(df['ConcentrationDifficulty'], categories=freq_order, ordered=True)
    df['AssignmentImpact'] = pd.Categorical(df['AssignmentImpact'], categories=impact_order, ordered=True)
    df['DaytimeFatigue'] = pd.Categorical(df['DaytimeFatigue'], categories=freq_order, ordered=True)
    
    return df, academic_order, insomnia_order, freq_order, impact_order
    
    # ==========================================
    # 4. HEADER
    # ==========================================
    st.title("Interpretation Dashboard: Impact of Sleep Related Issues on Academic Performance")
    st.markdown("### How sleep-related issues affect focus, fatigue, assignments, and performance")
    st.divider()

    # ==========================================
    # 5. KEY METRICS
    # ==========================================
    st.subheader("Key Findings: The Impact of Severe Insomnia")

    severe_df = df[df["Insomnia_Category"] == "Severe Insomnia"]

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
    # 6. CHART 1 – CONCENTRATION
    # ==========================================
    ctab = pd.crosstab(df["Insomnia_Category"], df["ConcentrationDifficulty"], dropna=False)
    cmelt = ctab.reset_index().melt("Insomnia_Category", var_name="Concentration", value_name="Count")

    fig1 = px.bar(
        cmelt, x="Insomnia_Category", y="Count", color="Concentration",
        barmode="group",
        category_orders={"Insomnia_Category": insomnia_order, "Concentration": freq_order},
        title="Concentration Difficulty by Insomnia Category",
        color_discrete_sequence=px.colors.sequential.Sunset
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.divider()

    # ==========================================
    # 7. CHART 2 – GPA vs INSOMNIA
    # ==========================================
    fig2 = px.box(
        df, x="GPA", y="InsomniaSeverity_index",
        color="GPA",
        title="Insomnia Severity Index Across GPA Categories",
        color_discrete_sequence=px.colors.sequential.Sunset
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.divider()

    # ==========================================
    # 8. CHART 3 – ASSIGNMENT IMPACT
    # ==========================================
    atab = pd.crosstab(df["Insomnia_Category"], df["AssignmentImpact"], dropna=False)
    amelt = atab.reset_index().melt("Insomnia_Category", var_name="Impact", value_name="Count")

    fig3 = px.bar(
        amelt, x="Insomnia_Category", y="Count", color="Impact",
        barmode="stack",
        category_orders={"Insomnia_Category": insomnia_order, "Impact": impact_order},
        title="Assignment Impact by Insomnia Category",
        color_discrete_sequence=px.colors.sequential.Sunset
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.divider()

    # ==========================================
    # 9. CHART 4 – FATIGUE
    # ==========================================
    ftab = pd.crosstab(df["Insomnia_Category"], df["DaytimeFatigue"], dropna=False)
    fmelt = ftab.reset_index().melt("Insomnia_Category", var_name="Fatigue", value_name="Count")

    fig4 = px.bar(
        fmelt, x="Insomnia_Category", y="Count", color="Fatigue",
        barmode="stack",
        category_orders={"Insomnia_Category": insomnia_order, "Fatigue": freq_order},
        title="Daytime Fatigue by Insomnia Severity",
        color_discrete_sequence=px.colors.sequential.Sunset
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.divider()

    # ==========================================
    # 10. CHART 5 – CORRELATION HEATMAP
    # ==========================================
    corr_cols = [
        "SleepHours_est", "InsomniaSeverity_index",
        "DaytimeFatigue_numeric", "ConcentrationDifficulty_numeric",
        "MissedClasses_numeric", "AcademicPerformance_numeric",
        "GPA_numeric", "CGPA_numeric"
    ]
    corr_cols = [c for c in corr_cols if c in df.columns]

    fig5 = px.imshow(
        df[corr_cols].corr(),
        text_auto=".2f",
        color_continuous_scale="Sunset",
        title="Correlation Heatmap: Sleep Issues vs Academic Outcomes"
    )
    st.plotly_chart(fig5, use_container_width=True)


# ==========================================
# STREAMLIT ENTRY POINT
# ==========================================
render()
