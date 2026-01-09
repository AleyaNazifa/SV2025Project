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

        # Metrics: severe insomnia group
