import streamlit as st
import numpy as np
from data_loader import (
    load_from_url,
    load_from_upload,
    ensure_engineered_columns,
    set_dataframe_in_session,
)

st.set_page_config(
    page_title="UMK Sleep Study", 
    layout="wide",
    page_icon="🌙",
    initial_sidebar_state="expanded"
)

from styles import apply_global_styles
apply_global_styles()

DEFAULT_GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSf4umx6QNDel99If8P2otizAHj7jEDxFIsqandbD0zYVzfDheZo2YVkK1_zknpDKjHnBuYWCINgcCe/pub?output=csv"

# SIDEBAR
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
        
        Analyzing relationships between:
        - Sleep quality
        - Academic performance
        - Lifestyle factors
        """)

# DATA LOADING
if mode == "🔄 Auto-Load":
    with st.spinner("Loading..."):
        try:
            df = load_from_url(DEFAULT_GOOGLE_SHEET_URL)
            st.sidebar.success(f"✅ {len(df)} responses")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.stop()
else:
    uploaded = st.sidebar.file_uploader("Choose CSV", type=["csv"])
    
    if uploaded is None:
        st.title("🌙 UMK Sleep Study")
        st.info("👈 Upload CSV to begin")
        st.stop()
    
    with st.spinner("Loading..."):
        df = load_from_upload(uploaded)
        st.sidebar.success(f"✅ {uploaded.name}")

df = ensure_engineered_columns(df)
set_dataframe_in_session(df)

# MAIN CONTENT
st.title("🌙 Sleep Quality & Academic Performance Study")
st.markdown("**Comprehensive Analysis Dashboard • UMK Research Project**")
st.markdown("---")

st.subheader("🎯 Research Objective")
st.info("""
To investigate the **relationship between sleep quality and academic performance** among UMK students, 
examining how insomnia severity, sleep patterns, and lifestyle factors correlate with educational 
outcomes and daily functioning.
""")

st.markdown("---")

st.subheader("📊 Key Insights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📝 Responses", f"{len(df):,}")

with col2:
    if "InsomniaSeverity_index" in df.columns:
        val = df['InsomniaSeverity_index'].mean()
        st.metric("😴 Insomnia", f"{val:.2f}")

with col3:
    if "AcademicImpact_index" in df.columns:
        val = df['AcademicImpact_index'].mean()
        st.metric("🎓 Impact", f"{val:.2f}")

with col4:
    if "SleepHours_est" in df.columns:
        val = df['SleepHours_est'].mean()
        st.metric("⏰ Sleep", f"{val:.1f}h")

st.markdown("---")

st.subheader("📈 Additional Metrics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    if "SleepQuality_score" in df.columns:
        st.metric("⭐ Quality", f"{df['SleepQuality_score'].mean():.2f}")

with c2:
    if "Stress_score" in df.columns:
        st.metric("😰 Stress", f"{df['Stress_score'].mean():.2f}")

with c3:
    if "AcademicPerformance_score" in df.columns:
        st.metric("📚 Performance", f"{df['AcademicPerformance_score'].mean():.2f}")

with c4:
    if "InsomniaSeverity_index" in df.columns and "AcademicImpact_index" in df.columns:
        corr_data = df[["InsomniaSeverity_index", "AcademicImpact_index"]].dropna()
        if len(corr_data) > 2:
            corr = np.corrcoef(corr_data["InsomniaSeverity_index"], corr_data["AcademicImpact_index"])[0, 1]
            st.metric("🔗 Correlation", f"{corr:+.3f}")

st.markdown("---")

with st.expander("🔍 Dataset Preview"):
    st.dataframe(df.head(10), use_container_width=True, height=350)
    st.caption(f"{len(df):,} responses • {df.shape[1]} features")

st.markdown("---")

st.subheader("🧭 Navigate")
st.info("""
Use sidebar to explore:
- 📊 **Insomnia Visualisation** - Charts & analysis
- 👥 **Subgroup Comparison** - Demographics
""")

st.success(f"✅ Ready • {len(df):,} responses")
