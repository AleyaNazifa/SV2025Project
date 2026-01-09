import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import display_sidebar_info, get_df
from cleaning_aelyana import prepare_aelyana_data

# NOTE: do not call st.set_page_config() here (app.py already does it)

def safe_mode(s: pd.Series, default="N/A"):
    s = s.dropna()
    return s.mode().iloc[0] if not s.empty else default


def render():
    display_sidebar_info()

    raw = get_df()
    df = prepare_aelyana_data(raw)

    if df is None or df.empty:
        st.error("No data available.")
        return

    academic_order = ["Below average", "Average", "Good", "Very good", "Excellent"]
    insomnia_order = ["Low / No Insomnia", "Moderate Insomnia", "Severe Insomnia"]
    freq_order = ["Never", "Rarely", "Sometimes", "Often", "Always"]
    impact_order = ["No impact", "Minor impact", "Moderate impact", "Major impact", "Severe impact"]

    # Categorical for order stability
    if "AcademicPerformance" in df.columns:
        df["AcademicPerformance"] = pd.Categorical(df["AcademicPerformance"], categories=academic_order, ordered=True)
    if "Insomnia_Category" in df.columns:
        df["Insomnia_Category"] = pd.Categorical(df["Insomnia_Category"], categories=insomnia_order, ordered=True)
    for c in ["ConcentrationDifficulty", "DaytimeFatigue"]:
        if c in df.columns:
            df[c] = pd.Categorical(df[c], categories=freq_order, ordered=True)
    if "AssignmentImpact" in df.columns:
        df["AssignmentImpact"] = pd.Categorical(df["AssignmentImpact"], categories=impact_order, ordered=True)

    st.title("Academic Impact Analysis (Aelyana)")
    st.markdown("### How sleep-related issues relate to focus, fatigue, assignments, and performance")
    st.divider()

    # -----------------------------
    # Metrics: severe insomnia group
    # -----------------------------
    severe = df[df["Insomnia_Category"] == "Severe Insomnia"] if "Insomnia_Category" in df.columns else df

    col1, col2, col3, col4 = st.columns(4)

    focus_risk = (
        severe["ConcentrationDifficulty"].isin(["Often", "Always"]).mean() * 100
        if "ConcentrationDifficulty" in severe.columns
        else 0.0
    )
    fatigue_risk = (
        severe["DaytimeFatigue"].isin(["Often", "Always"]).mean() * 100
        if "DaytimeFatigue" in severe.columns
        else 0.0
    )
    perf_level = safe_mode(severe["AcademicPerformance"]) if "AcademicPerformance" in severe.columns else "N/A"
    assign_risk = (
        severe["AssignmentImpact"].isin(["Major impact", "Severe impact"]).mean() * 100
        if "AssignmentImpact" in severe.columns
        else 0.0
    )

    col1.metric("🧠 Concentration Difficulty", f"{focus_risk:.1f}%")
    col2.metric("😫 Severe Academic Fatigue", f"{fatigue_risk:.1f}%")
    col3.metric("📉 Academic Performance Level", perf_level)
    col4.metric("📝 Assignment Performance Risk", f"{assign_risk:.1f}%")

    st.divider()

    # -----------------------------
    # Chart 1
    # -----------------------------
    if {"Insomnia_Category", "ConcentrationDifficulty"}.issubset(df.columns):
        tab = pd.crosstab(df["Insomnia_Category"], df["ConcentrationDifficulty"], dropna=False)
        melted = tab.reset_index().melt(
            id_vars="Insomnia_Category",
            var_name="ConcentrationDifficulty",
            value_name="Count",
        )
        fig = px.bar(
            melted,
            x="Insomnia_Category",
            y="Count",
            color="ConcentrationDifficulty",
            barmode="group",
            title="Concentration Difficulty by Insomnia Category",
            category_orders={"Insomnia_Category": insomnia_order, "ConcentrationDifficulty": freq_order},
            labels={"Count": "Number of Students", "Insomnia_Category": "Insomnia Level"},
        )
        st.plotly_chart(fig, use_container_width=True)
        st.divider()
    else:
        st.warning("Missing columns for Chart 1.")

    # -----------------------------
    # Chart 2
    # -----------------------------
    if {"GPA", "InsomniaSeverity_index"}.issubset(df.columns):
        gpa_order = sorted(df["GPA"].dropna().unique().tolist())
        fig = px.box(
            df,
            x="GPA",
            y="InsomniaSeverity_index",
            color="GPA",
            title="Insomnia Severity Index Across GPA Categories",
            category_orders={"GPA": gpa_order},
            points="outliers",
        )
        fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        st.divider()
    else:
        st.warning("Missing columns for Chart 2.")

    # -----------------------------
    # Chart 3
    # -----------------------------
    if {"Insomnia_Category", "AssignmentImpact"}.issubset(df.columns):
        tab = pd.crosstab(df["Insomnia_Category"], df["AssignmentImpact"], dropna=False)
        melted = tab.reset_index().melt(
            id_vars="Insomnia_Category",
            var_name="AssignmentImpact",
            value_name="Student_Count",
        )
        fig = px.bar(
            melted,
            x="Insomnia_Category",
            y="Student_Count",
            color="AssignmentImpact",
            title="Assignment Impact by Insomnia Category",
            category_orders={"Insomnia_Category": insomnia_order, "AssignmentImpact": impact_order},
            barmode="stack",
            labels={"Student_Count": "Number of Students"},
        )
        st.plotly_chart(fig, use_container_width=True)
        st.divider()
    else:
        st.warning("Missing columns for Chart 3.")

    # -----------------------------
    # Chart 4
    # -----------------------------
    if {"Insomnia_Category", "DaytimeFatigue"}.issubset(df.columns):
        tab = pd.crosstab(df["Insomnia_Category"], df["DaytimeFatigue"], dropna=False)
        melted = tab.reset_index().melt(
            id_vars="Insomnia_Category",
            var_name="DaytimeFatigue",
            value_name="Count",
        )
        fig = px.bar(
            melted,
            x="Insomnia_Category",
            y="Count",
            color="DaytimeFatigue",
            title="Fatigue Level by Insomnia Severity",
            category_orders={"Insomnia_Category": insomnia_order, "DaytimeFatigue": freq_order},
            barmode="stack",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.divider()
    else:
        st.warning("Missing columns for Chart 4.")

    # -----------------------------
    # Chart 5
    # -----------------------------
    if {"Insomnia_Category", "AcademicPerformance"}.issubset(df.columns):
        fig = px.box(
            df,
            x="Insomnia_Category",
            y="AcademicPerformance",
            color="Insomnia_Category",
            title="Academic Performance by Insomnia Severity",
            category_orders={"Insomnia_Category": insomnia_order, "AcademicPerformance": academic_order},
            points="outliers",
        )
        fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Missing columns for Chart 5.")


render()



