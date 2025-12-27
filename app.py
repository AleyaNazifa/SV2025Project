import streamlit as st
from data_loader import (
    load_from_url,
    load_from_upload,
    ensure_engineered_columns,
    set_dataframe_in_session,
)

# MUST BE FIRST - Page config
st.set_page_config(
    page_title="UMK Sleep & Academic Dashboard", 
    layout="wide",
    page_icon="🌙",
    initial_sidebar_state="expanded"
)

# ===== CONFIGURATION: Set your Google Sheet URL here =====
# This URL will auto-load data without user input
DEFAULT_GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSf4umx6QNDel99If8P2otizAHj7jEDxFIsqandbD0zYVzfDheZo2YVkK1_zknpDKjHnBuYWCINgcCe/pub?output=csv"
# ==========================================================

# Professional styling with better colors
st.markdown("""
<style>
    /* Force light theme */
    .stApp {
        background-color: #fafbfc;
    }
    
    /* Professional sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        border-right: 1px solid #d1d5db;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: transparent;
        padding-top: 1.5rem;
    }
    
    /* Sidebar headings - professional gray tones */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span {
        color: #4b5563 !important;
    }
    
    section[data-testid="stSidebar"] .stCaption {
        color: #6b7280 !important;
        font-size: 0.8rem !important;
    }
    
    /* Radio buttons styling */
    section[data-testid="stSidebar"] .stRadio > div {
        background-color: white;
        padding: 0.5rem;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        color: #374151 !important;
    }
    
    /* Professional button - blue accent */
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        width: 100%;
        border-radius: 8px;
        padding: 0.7rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
        transition: all 0.2s;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.4);
        transform: translateY(-1px);
    }
    
    /* Dividers */
    section[data-testid="stSidebar"] hr {
        border-color: #e5e7eb;
        margin: 1.2rem 0;
    }
    
    /* Expander styling */
    section[data-testid="stSidebar"] .streamlit-expanderHeader {
        background-color: #f3f4f6;
        border-radius: 6px;
        color: #374151 !important;
        font-weight: 500;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: #fafbfc;
        padding: 2.5rem 1.5rem;
    }
    
    /* Main headings */
    .main h1 {
        color: #111827;
        font-weight: 700;
        font-size: 2.25rem;
        margin-bottom: 0.5rem;
    }
    
    .main h2 {
        color: #1f2937;
        font-weight: 600;
        font-size: 1.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    .main h3 {
        color: #374151;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    .main p {
        color: #4b5563;
        line-height: 1.7;
    }
    
    /* Professional stat cards */
    .stat-card {
        background: white;
        border-radius: 10px;
        padding: 1.75rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
        border: 1px solid #e5e7eb;
        text-align: center;
        transition: all 0.2s;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06);
    }
    
    .stat-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
    }
    
    .stat-value {
        font-size: 2.25rem;
        font-weight: 700;
        color: #111827;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: #6b7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Objective box - professional blue accent */
    .objective-box {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 10px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 1px 3px rgba(59, 130, 246, 0.1);
    }
    
    .objective-box h3 {
        color: #1e40af !important;
        margin-top: 0 !important;
    }
    
    .objective-box p {
        color: #1f2937 !important;
    }
    
    /* Navigation cards */
    .nav-card {
        background: white;
        border-radius: 10px;
        padding: 1.75rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
        border: 1px solid #e5e7eb;
        transition: all 0.2s;
        height: 100%;
    }
    
    .nav-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06);
        transform: translateY(-2px);
        border-color: #3b82f6;
    }
    
    .nav-card h3 {
        color: #3b82f6 !important;
        margin-top: 0 !important;
        font-size: 1.1rem !important;
    }
    
    .nav-card p {
        color: #6b7280 !important;
        margin-bottom: 0 !important;
        font-size: 0.9rem !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #111827;
        font-size: 1.75rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6b7280;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    /* Alert boxes */
    .stSuccess {
        background-color: #d1fae5 !important;
        border-left: 4px solid #10b981 !important;
        color: #065f46 !important;
    }
    
    .stInfo {
        background-color: #dbeafe !important;
        border-left: 4px solid #3b82f6 !important;
        color: #1e40af !important;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Data Source")
    st.caption("Choose how to load your data")
    
    mode = st.radio(
        "Select input method",
        ["🔄 Auto-Load (Google Sheet)", "📁 Manual Upload"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    st.markdown("### 🔄 Data Management")
    if st.button("Refresh Data", use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.rerun()
    st.caption("Click to reload latest data")
    
    st.divider()
    
    with st.expander("❓ Help & Info"):
        st.markdown("""
        **Auto-Load Mode:**
        - Data loads automatically
        - Updates every 5 minutes
        - No manual input needed
        
        **Manual Upload:**
        - Upload your own CSV
        - Full control over data
        - Useful for testing
        """)
    
    st.markdown("---")
    st.caption("**UMK Sleep Study Dashboard**")
    st.caption("Version 1.0 • Last updated: 2024")

# Load data based on mode
if mode == "🔄 Auto-Load (Google Sheet)":
    # Automatically load from the configured URL
    with st.spinner("📥 Loading data from Google Sheets..."):
        try:
            df = load_from_url(DEFAULT_GOOGLE_SHEET_URL)
            with st.sidebar:
                st.success("✅ Data auto-loaded")
                st.caption(f"{len(df)} responses loaded")
        except Exception as e:
            st.error(f"❌ Failed to load data: {str(e)}")
            st.info("💡 Try switching to Manual Upload mode or check your internet connection")
            st.stop()
else:
    with st.sidebar:
        st.markdown("### 📤 Upload File")
        uploaded = st.file_uploader(
            "Choose CSV file",
            type=["csv"],
            help="Maximum file size: 200MB"
        )
    
    if uploaded is None:
        st.title("🌙 UMK Sleep & Academic Study")
        st.markdown("**Research Dashboard for Sleep Quality Analysis**")
        st.divider()
        st.info("👈 **Upload your CSV file in the sidebar to begin analysis**")
        st.stop()
    
    with st.spinner("📥 Processing file..."):
        df = load_from_upload(uploaded)
        with st.sidebar:
            st.success(f"✅ {uploaded.name}")
            st.caption(f"{len(df)} responses loaded")

# Process data
df = ensure_engineered_columns(df)
set_dataframe_in_session(df)

# Main Dashboard
st.title("🌙 UMK Sleep & Academic Study Dashboard")
st.markdown("**Comprehensive Analysis of Sleep Quality and Academic Performance**")
st.divider()

# Objective
st.markdown("""
<div class="objective-box">
    <h3>🎯 Research Objective</h3>
    <p style='font-size: 1.05rem; line-height: 1.8; margin-bottom: 0;'>
        Analyze the <strong>relationship between sleep quality and academic performance</strong> among 
        UMK students to identify correlations between insomnia severity, sleep patterns, 
        lifestyle factors, and educational outcomes. This research aims to provide evidence-based 
        insights for improving student wellness and academic success.
    </p>
</div>
""", unsafe_allow_html=True)

# Summary Statistics
st.markdown("## 📊 Key Statistics Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-value">{len(df)}</div>
        <div class="stat-label">Total Responses</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if "InsomniaSeverity_index" in df.columns:
        val = df['InsomniaSeverity_index'].mean()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">😴</div>
            <div class="stat-value">{val:.2f}</div>
            <div class="stat-label">Insomnia Severity</div>
        </div>
        """, unsafe_allow_html=True)

with col3:
    if "AcademicImpact_index" in df.columns:
        val = df['AcademicImpact_index'].mean()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">🎓</div>
            <div class="stat-value">{val:.2f}</div>
            <div class="stat-label">Academic Impact</div>
        </div>
        """, unsafe_allow_html=True)

with col4:
    if "SleepHours_est" in df.columns:
        val = df['SleepHours_est'].mean()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">⏰</div>
            <div class="stat-value">{val:.1f}h</div>
            <div class="stat-label">Sleep Duration</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Additional metrics
c1, c2, c3 = st.columns(3)
with c1:
    if "SleepQuality_score" in df.columns:
        st.metric("⭐ Sleep Quality", f"{df['SleepQuality_score'].mean():.2f} / 5")
with c2:
    if "Stress_score" in df.columns:
        st.metric("😰 Stress Level", f"{df['Stress_score'].mean():.2f} / 4")
with c3:
    if "AcademicPerformance_score" in df.columns:
        st.metric("📚 Academic Performance", f"{df['AcademicPerformance_score'].mean():.2f} / 5")

st.divider()

# Navigation
st.markdown("## 🧭 Explore Analysis Sections")

nc1, nc2, nc3 = st.columns(3)

with nc1:
    st.markdown("""
    <div class="nav-card">
        <h3>🏠 Home</h3>
        <p>Dataset overview, demographics, and detailed statistics about the survey responses</p>
    </div>
    """, unsafe_allow_html=True)

with nc2:
    st.markdown("""
    <div class="nav-card">
        <h3>📈 Visualizations</h3>
        <p>Comprehensive charts, graphs, and statistical analysis of sleep patterns</p>
    </div>
    """, unsafe_allow_html=True)

with nc3:
    st.markdown("""
    <div class="nav-card">
        <h3>👥 Comparisons</h3>
        <p>Compare metrics across demographics, faculties, and student groups</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.success(f"✅ Dashboard ready • {len(df)} responses • {df.shape[1]} features analyzed • Auto-refresh enabled")

with st.expander("ℹ️ About This Dashboard"):
    st.markdown("""
    **UMK Sleep & Academic Performance Research Dashboard**
    
    This interactive dashboard provides comprehensive analysis of sleep quality and its impact 
    on academic performance among Universiti Malaysia Kelantan students. Features include:
    
    - **Real-time data synchronization** from Google Sheets
    - **Interactive visualizations** with filtering capabilities
    - **Statistical analysis** of sleep patterns and academic outcomes
    - **Demographic comparisons** across different student groups
    - **Correlation analysis** between lifestyle factors and performance
    
    Data is automatically refreshed every 5 minutes to ensure you always have the latest insights.
    """)
