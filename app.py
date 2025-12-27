import streamlit as st
from data_loader import (
    load_from_url,
    load_from_upload,
    ensure_engineered_columns,
    set_dataframe_in_session,
)

# ===== CONFIGURATION =====
DEFAULT_GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSf4umx6QNDel99If8P2otizAHj7jEDxFIsqandbD0zYVzfDheZo2YVkK1_zknpDKjHnBuYWCINgcCe/pub?output=csv"

st.set_page_config(
    page_title="UMK Sleep Study", 
    layout="wide",
    page_icon="🌙",
    initial_sidebar_state="expanded"
)

# Modern Professional Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main .block-container {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 3rem 2rem;
        margin-top: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
    }
    
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    
    .objective-card {
        background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
        border-left: 5px solid #667eea;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.1);
    }
    
    .stat-box {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 2px solid #f1f5f9;
        transition: all 0.3s;
    }
    
    .stat-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    
    .stat-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.875rem;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

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
st.markdown("""
<div class="objective-card">
    <h3 style="color: #5046e5; margin-top: 0;">🎯 Research Objective</h3>
    <p style="color: #1e293b; font-size: 1.1rem; line-height: 1.8; margin-bottom: 0;">
        To investigate the <strong>relationship between sleep quality and academic performance</strong> 
        among UMK students, examining how insomnia severity, sleep patterns, and lifestyle factors 
        correlate with educational outcomes and daily functioning.
    </p>
</div>
""", unsafe_allow_html=True)

# Key Statistics Cards
st.markdown("## 📊 Key Insights at a Glance")
st.markdown("")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-icon">📝</div>
        <div class="stat-value">{len(df)}</div>
        <div class="stat-label">Total Responses</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if "InsomniaSeverity_index" in df.columns:
        val = df['InsomniaSeverity_index'].mean()
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-icon">😴</div>
            <div class="stat-value">{val:.2f}</div>
            <div class="stat-label">Avg Insomnia Index</div>
        </div>
        """, unsafe_allow_html=True)

with col3:
    if "AcademicImpact_index" in df.columns:
        val = df['AcademicImpact_index'].mean()
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-icon">🎓</div>
            <div class="stat-value">{val:.2f}</div>
            <div class="stat-label">Academic Impact</div>
        </div>
        """, unsafe_allow_html=True)

with col4:
    if "SleepHours_est" in df.columns:
        val = df['SleepHours_est'].mean()
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-icon">⏰</div>
            <div class="stat-value">{val:.1f}h</div>
            <div class="stat-label">Avg Sleep Hours</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Additional Metrics Row
st.markdown("### 📈 Additional Metrics")
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
            import numpy as np
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
st.markdown("## 🧭 Navigation")
st.info("""
**Ready to explore!** Use the sidebar to navigate between different analysis pages:
- 🏠 **Home** - Overview and statistics (you are here)
- 📊 **Visualizations** - Interactive charts and correlations
- 👥 **Comparisons** - Demographic analysis
""")

st.success(f"✅ Dashboard ready • {len(df)} responses loaded • All features engineered")
