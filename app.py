import streamlit as st
from data_loader import (
    load_from_url,
    load_from_upload,
    ensure_engineered_columns,
    set_dataframe_in_session,
)

# ===== CONFIGURATION =====
# Set your Google Sheet CSV URL here for auto-loading
DEFAULT_GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSf4umx6QNDel99If8P2otizAHj7jEDxFIsqandbD0zYVzfDheZo2YVkK1_zknpDKjHnBuYWCINgcCe/pub?output=csv"
# =========================

# Page configuration
st.set_page_config(
    page_title="UMK Sleep & Academic Dashboard", 
    layout="wide",
    page_icon="🌙",
    initial_sidebar_state="expanded"
)

# Professional styling
st.markdown("""
<style>
    /* Import professional font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global font */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main app background */
    .stApp {
        background-color: #fafbfc !important;
    }
    
    /* Main content */
    .main {
        background-color: #fafbfc !important;
    }
    
    .main .block-container {
        background-color: #fafbfc !important;
        padding: 2.5rem 1.5rem;
        max-width: 1400px;
    }
    
    /* Sidebar professional styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%) !important;
        border-right: 1px solid #dee2e6 !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: transparent !important;
        padding-top: 2rem;
    }
    
    /* Sidebar text colors */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #1f2937 !important;
    }
    
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span {
        color: #4b5563 !important;
    }
    
    /* Sidebar radio buttons */
    section[data-testid="stSidebar"] .stRadio > div {
        background-color: white;
        padding: 0.75rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
    
    /* Sidebar button */
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
        transition: all 0.2s;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.4);
        transform: translateY(-1px);
    }
    
    /* Main content headings */
    .main h1 {
        color: #111827 !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
    }
    
    .main h2 {
        color: #1f2937 !important;
        font-weight: 600 !important;
        font-size: 1.75rem !important;
        margin-top: 2rem !important;
    }
    
    .main h3 {
        color: #374151 !important;
        font-weight: 600 !important;
    }
    
    .main p {
        color: #4b5563 !important;
        line-height: 1.7;
    }
    
    /* Stat cards */
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.15), 0 2px 4px rgba(0,0,0,0.08);
    }
    
    .stat-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #111827;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Objective box */
    .objective-box {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 1px 3px rgba(59, 130, 246, 0.15);
    }
    
    .objective-box h3 {
        color: #1e40af !important;
        margin-top: 0 !important;
        font-size: 1.25rem !important;
    }
    
    .objective-box p {
        color: #1f2937 !important;
        font-size: 1.05rem;
        line-height: 1.8;
    }
    
    /* Navigation cards */
    .nav-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .nav-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.15), 0 2px 4px rgba(0,0,0,0.08);
        transform: translateY(-2px);
        border-color: #3b82f6;
    }
    
    .nav-card h3 {
        color: #3b82f6 !important;
        margin-top: 0 !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
    }
    
    .nav-card p {
        color: #6b7280 !important;
        margin-bottom: 0 !important;
        font-size: 0.9rem !important;
        line-height: 1.6;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #111827 !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }
    
    /* Alerts */
    .stSuccess {
        background-color: #d1fae5 !important;
        border-left: 4px solid #10b981 !important;
        color: #065f46 !important;
        border-radius: 8px !important;
    }
    
    .stInfo {
        background-color: #dbeafe !important;
        border-left: 4px solid #3b82f6 !important;
        color: #1e40af !important;
        border-radius: 8px !important;
    }
    
    /* Dividers */
    hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 2rem 0;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### 📊 Data Source")
    st.caption("Select how to load your data")
    
    mode = st.radio(
        "Mode",
        ["🔄 Auto-Load (Google Sheet)", "📁 Manual Upload"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    st.markdown("### 🔄 Data Management")
    if st.button("Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.caption("Click to reload latest data")
    
    st.divider()
    
    with st.expander("❓ Help"):
        st.markdown("""
        **Auto-Load:**
        - Data loads automatically
        - Updates every 5 minutes
        
        **Manual Upload:**
        - Upload your own CSV
        - Full control over data
        """)
    
    st.markdown("---")
    st.caption("UMK Sleep Study v1.0")

# ===== DATA LOADING =====
if mode == "🔄 Auto-Load (Google Sheet)":
    with st.spinner("📥 Loading data..."):
        try:
            df = load_from_url(DEFAULT_GOOGLE_SHEET_URL)
            with st.sidebar:
                st.success("✅ Data loaded")
                st.caption(f"{len(df)} responses")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.stop()
else:
    with st.sidebar:
        st.markdown("### 📤 Upload CSV")
        uploaded = st.file_uploader("Choose file", type=["csv"])
    
    if uploaded is None:
        st.title("🌙 UMK Sleep Study")
        st.markdown("**Research Dashboard**")
        st.divider()
        st.info("👈 Upload CSV to begin")
        st.stop()
    
    with st.spinner("📥 Processing..."):
        df = load_from_upload(uploaded)
        with st.sidebar:
            st.success(f"✅ {uploaded.name}")

# Process data
df = ensure_engineered_columns(df)
set_dataframe_in_session(df)

# ===== MAIN DASHBOARD =====
st.title("🌙 UMK Sleep & Academic Study")
st.markdown("**Comprehensive Analysis of Sleep Quality and Academic Performance**")
st.divider()

# Objective
st.markdown("""
<div class="objective-box">
    <h3>🎯 Research Objective</h3>
    <p>
        Analyze the <strong>relationship between sleep quality and academic performance</strong> among 
        UMK students to identify correlations between insomnia severity, sleep patterns, 
        lifestyle factors, and educational outcomes.
    </p>
</div>
""", unsafe_allow_html=True)

# Key Stats
st.markdown("## 📊 Key Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-value">{len(df)}</div>
        <div class="stat-label">Responses</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if "InsomniaSeverity_index" in df.columns:
        val = df['InsomniaSeverity_index'].mean()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">😴</div>
            <div class="stat-value">{val:.2f}</div>
            <div class="stat-label">Insomnia Index</div>
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

# Additional Metrics
c1, c2, c3 = st.columns(3)
with c1:
    if "SleepQuality_score" in df.columns:
        st.metric("⭐ Sleep Quality", f"{df['SleepQuality_score'].mean():.2f} / 5")
with c2:
    if "Stress_score" in df.columns:
        st.metric("😰 Stress Level", f"{df['Stress_score'].mean():.2f} / 4")
with c3:
    if "AcademicPerformance_score" in df.columns:
        st.metric("📚 Performance", f"{df['AcademicPerformance_score'].mean():.2f} / 5")

st.divider()

# Navigation
st.markdown("## 🧭 Explore Sections")

nc1, nc2, nc3 = st.columns(3)

with nc1:
    st.markdown("""
    <div class="nav-card">
        <h3>🏠 Home</h3>
        <p>Dataset overview and detailed statistics</p>
    </div>
    """, unsafe_allow_html=True)

with nc2:
    st.markdown("""
    <div class="nav-card">
        <h3>📈 Visualizations</h3>
        <p>Comprehensive charts and analysis</p>
    </div>
    """, unsafe_allow_html=True)

with nc3:
    st.markdown("""
    <div class="nav-card">
        <h3>👥 Comparisons</h3>
        <p>Compare across demographics</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.success(f"✅ Ready • {len(df)} responses • {df.shape[1]} features")
