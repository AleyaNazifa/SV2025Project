"""
Main entry point for UMK Sleep Study Dashboard
"""

import streamlit as st
import numpy as np
from data_loader import (
    load_from_url,
    load_from_upload,
    ensure_engineered_columns,
    set_dataframe_in_session,
)

# Must be first Streamlit command
st.set_page_config(
    page_title="UMK Sleep Study", 
    layout="wide",
    page_icon="🌙",
    initial_sidebar_state="expanded"
)

# Import and apply styles AFTER set_page_config
from styles import apply_global_styles
apply_global_styles()

# ===== CONFIGURATION =====
DEFAULT_GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSf4umx6QNDel99If8P2otizAHj7jEDxFIsqandbD0zYVzfDheZo2YVkK1_zknpDKjHnBuYWCINgcCe/pub?output=csv"

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("# 🌙 Sleep Study")
    st.markdown("### Data Source")
    
    mode = st.radio(
        "Select Mode",
        ["🔄 Auto-Load", "📁 Upload CSV"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    
    with st.expander("ℹ️ About"):
        st.markdown("""
        **UMK Sleep Study Dashboard**
        
        Analyzing the relationship between:
        - Sleep quality patterns
        - Academic performance
        - Lifestyle factors
        
        **Features:**
        - Real-time data loading
        - Interactive visualizations
        - Statistical analysis
        """)

# ===== DATA LOADING =====
if mode == "🔄 Auto-Load":
    with st.spinner("📥 Loading data from Google Sheets..."):
        try:
            df = load_from_url(DEFAULT_GOOGLE_SHEET_URL)
            with st.sidebar:
                st.success(f"✅ Loaded {len(df)} responses")
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            st.stop()
else:
    with st.sidebar:
        uploaded = st.file_uploader("Choose your CSV file", type=["csv"])
    
    if uploaded is None:
        st.title("🌙 UMK Sleep & Academic Study")
        st.markdown("---")
        st.info("👈 Please upload a CSV file to begin analysis")
        st.stop()
    
    with st.spinner("📥 Processing your data..."):
        df = load_from_upload(uploaded)
        with st.sidebar:
            st.success(f"✅ Uploaded {uploaded.name}")

# Process data
df = ensure_engineered_columns(df)
set_dataframe_in_session(df)

# ===== MAIN DASHBOARD =====
st.title("🌙 Sleep Quality & Academic Performance Study")
st.markdown("**Comprehensive Analysis Dashboard • UMK Research Project**")
st.markdown("---")

# Objective Section
st.subheader("🎯 Research Objective")
st.info("""
**To investigate the relationship between sleep quality and academic performance** among UMK students, 
examining how insomnia severity, sleep patterns, and lifestyle factors correlate with educational 
outcomes and daily functioning.
""")

st.markdown("---")

# Key Statistics
st.subheader("📊 Key Insights at a Glance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📝 Total Responses", 
        value=f"{len(df):,}",
        help="Total number of survey responses"
    )

with col2:
    if "InsomniaSeverity_index" in df.columns:
        val = df['InsomniaSeverity_index'].mean()
        st.metric(
            label="😴 Insomnia Index", 
            value=f"{val:.2f}",
            help="Average insomnia severity index (0-4 scale)"
        )

with col3:
    if "AcademicImpact_index" in df.columns:
        val = df['AcademicImpact_index'].mean()
        st.metric(
            label="🎓 Academic Impact", 
            value=f"{val:.2f}",
            help="Average academic impact score"
        )

with col4:
    if "SleepHours_est" in df.columns:
        val = df['SleepHours_est'].mean()
        st.metric(
            label="⏰ Avg Sleep", 
            value=f"{val:.1f}h",
            help="Average sleep hours per night"
        )

st.markdown("---")

# Additional Metrics Row
st.subheader("📈 Additional Metrics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    if "SleepQuality_score" in df.columns:
        st.metric(
            "⭐ Sleep Quality", 
            f"{df['SleepQuality_score'].mean():.2f}",
            help="Average sleep quality rating (1-5 scale)"
        )

with c2:
    if "Stress_score" in df.columns:
        st.metric(
            "😰 Stress Level", 
            f"{df['Stress_score'].mean():.2f}",
            help="Average stress level (1-4 scale)"
        )

with c3:
    if "AcademicPerformance_score" in df.columns:
        st.metric(
            "📚 Performance", 
            f"{df['AcademicPerformance_score'].mean():.2f}",
            help="Average academic performance (1-5 scale)"
        )

with c4:
    if "InsomniaSeverity_index" in df.columns and "AcademicImpact_index" in df.columns:
        corr_data = df[["InsomniaSeverity_index", "AcademicImpact_index"]].dropna()
        if len(corr_data) > 2:
            corr = np.corrcoef(corr_data["InsomniaSeverity_index"], corr_data["AcademicImpact_index"])[0, 1]
            st.metric(
                "🔗 Correlation", 
                f"{corr:+.3f}",
                help="Correlation between insomnia and academic impact"
            )

st.markdown("---")

# Data Preview
with st.expander("🔍 View Dataset Preview"):
    st.dataframe(
        df.head(10), 
        use_container_width=True,
        height=350
    )
    st.caption(f"Showing 10 of {len(df):,} total responses • {df.shape[1]} features analyzed")

st.markdown("---")

# Navigation Info
st.subheader("🧭 Navigate to Other Pages")
st.info("""
**Use the sidebar to explore different sections:**
- 📊 **Insomnia Visualisation** - Interactive charts and analysis
- 👥 **Subgroup Comparison** - Compare across demographics
""")

st.success(f"✅ Dashboard ready • {len(df):,} responses loaded • All features engineered")
