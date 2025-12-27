import streamlit as st
from data_loader import (
    load_from_url,
    load_from_upload,
    ensure_engineered_columns,
    set_dataframe_in_session,
)

# MUST BE FIRST - Page config with light theme
st.set_page_config(
    page_title="UMK Sleep & Academic Dashboard", 
    layout="wide",
    page_icon="🌙",
    initial_sidebar_state="expanded"
)

# Inject CSS to force light theme and professional styling
st.markdown("""
<style>
    /* Force light theme */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Sidebar white background */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e9ecef;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: #ffffff;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: #f8f9fa;
        padding: 2rem 1rem;
    }
    
    /* Sidebar text colors */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #212529 !important;
    }
    
    /* Main content text */
    .main h1 {
        color: #212529;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .main h2 {
        color: #343a40;
        font-weight: 600;
        font-size: 1.75rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    .main h3 {
        color: #495057;
        font-weight: 600;
        font-size: 1.25rem;
    }
    
    .main p {
        color: #495057;
        line-height: 1.6;
    }
    
    /* Professional card styling */
    .stat-card {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        border: 1px solid #dee2e6;
        text-align: center;
        transition: transform 0.2s;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    
    .stat-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #212529;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: #6c757d;
        font-weight: 500;
    }
    
    /* Info boxes */
    .info-box {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
    
    .objective-box {
        background: #e7f3ff;
        border-left: 4px solid #0d6efd;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #0d6efd;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: background-color 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #0b5ed7;
    }
    
    /* Radio buttons */
    .stRadio > label {
        font-weight: 500;
        color: #212529;
    }
    
    /* Text inputs */
    .stTextInput input {
        border: 1px solid #ced4da;
        border-radius: 6px;
        padding: 0.5rem;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #212529;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6c757d;
        font-size: 0.875rem;
    }
    
    /* Navigation cards */
    .nav-card {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        border: 1px solid #dee2e6;
        transition: all 0.2s;
    }
    
    .nav-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #dee2e6;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Header
    st.markdown("### ⚙️ Dashboard Settings")
    st.caption("Configure your data source and preferences")
    st.divider()
    
    # Data source selection
    st.markdown("**📊 Data Source**")
    mode = st.radio(
        "Select input method",
        ["🌐 Google Sheet (Live)", "📁 CSV Upload"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Refresh button
    st.markdown("**🔄 Data Management**")
    if st.button("Refresh Data", use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.rerun()
    
    st.caption("Click to reload latest data")
    st.divider()
    
    # Help section
    with st.expander("❓ Need Help?"):
        st.markdown("""
        **Quick Guide:**
        - Select data source above
        - Enter URL or upload file
        - Navigate using menu
        - Use filters in analysis pages
        """)
    
    # Footer
    st.markdown("---")
    st.caption("UMK Sleep Study Dashboard v1.0")
    st.caption("Data auto-syncs every 5 minutes")

# Load data
if mode == "🌐 Google Sheet (Live)":
    with st.sidebar:
        st.markdown("**🔗 Connection Settings**")
        st.caption("Enter your published Google Sheet URL")
        
        csv_url = st.text_input(
            "Google Sheet URL",
            placeholder="Paste CSV URL here...",
            help="Go to File → Share → Publish to web → Select CSV"
        )
        
        if csv_url.strip():
            st.success("✅ URL detected")
        else:
            st.info("⏳ Waiting for URL")
    
    if not csv_url.strip():
        st.title("🌙 UMK Insomnia & Educational Outcomes")
        st.markdown("**Research Dashboard for Sleep Quality and Academic Performance**")
        st.divider()
        
        st.info("👈 **Enter your Google Sheet CSV URL in the sidebar to get started**")
        
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("📖 How to get CSV URL"):
                st.markdown("""
                1. Open your Google Sheet
                2. **File** → **Share** → **Publish to web**
                3. Choose **CSV** format
                4. Copy the URL
                5. Paste in sidebar
                """)
        
        with col2:
            with st.expander("📊 Data Requirements"):
                st.markdown("""
                Your CSV should include:
                - Sleep measurements
                - Academic metrics
                - Demographics
                - Lifestyle data
                """)
        st.stop()
    
    with st.spinner("📥 Loading from Google Sheets..."):
        df = load_from_url(csv_url.strip())
        
else:
    with st.sidebar:
        st.markdown("**📤 File Upload**")
        st.caption("Upload your CSV data file")
        
        uploaded = st.file_uploader(
            "Choose file",
            type=["csv"],
            help="Maximum file size: 200MB"
        )
        
        if uploaded:
            st.success(f"✅ {uploaded.name}")
        else:
            st.info("⏳ No file selected")
    
    if uploaded is None:
        st.title("🌙 UMK Insomnia & Educational Outcomes")
        st.markdown("**Research Dashboard for Sleep Quality and Academic Performance**")
        st.divider()
        st.info("👈 **Upload your CSV file in the sidebar**")
        st.stop()
    
    with st.spinner("📥 Processing file..."):
        df = load_from_upload(uploaded)

# Process
df = ensure_engineered_columns(df)
set_dataframe_in_session(df)

# Main Dashboard
st.title("🌙 UMK Sleep & Academic Study Dashboard")
st.markdown("**Research on Sleep Quality and Academic Performance Among UMK Students (2024)**")
st.divider()

# Objective
st.markdown("""
<div class="objective-box">
    <h3 style='color: #0d6efd; margin-top: 0;'>🎯 Research Objective</h3>
    <p style='color: #212529; font-size: 1.05rem; margin-bottom: 0;'>
        Analyze the <strong>relationship between sleep quality and academic performance</strong> among 
        UMK students to identify correlations between insomnia severity, sleep patterns, 
        lifestyle factors, and educational outcomes.
    </p>
</div>
""", unsafe_allow_html=True)

# Summary Stats
st.markdown("## 📊 Key Statistics")

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
            <div class="stat-label">Avg Insomnia Severity</div>
        </div>
        """, unsafe_allow_html=True)

with col3:
    if "AcademicImpact_index" in df.columns:
        val = df['AcademicImpact_index'].mean()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">🎓</div>
            <div class="stat-value">{val:.2f}</div>
            <div class="stat-label">Avg Academic Impact</div>
        </div>
        """, unsafe_allow_html=True)

with col4:
    if "SleepHours_est" in df.columns:
        val = df['SleepHours_est'].mean()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">⏰</div>
            <div class="stat-value">{val:.1f}h</div>
            <div class="stat-label">Avg Sleep Duration</div>
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
st.markdown("## 🧭 Explore Analysis")

nc1, nc2, nc3 = st.columns(3)

with nc1:
    st.markdown("""
    <div class="nav-card">
        <h3 style='color: #0d6efd; margin-top: 0;'>🏠 Home</h3>
        <p style='color: #6c757d; margin-bottom: 0;'>Dataset overview and detailed statistics</p>
    </div>
    """, unsafe_allow_html=True)

with nc2:
    st.markdown("""
    <div class="nav-card">
        <h3 style='color: #0d6efd; margin-top: 0;'>📈 Visualisation</h3>
        <p style='color: #6c757d; margin-bottom: 0;'>Comprehensive charts and analysis</p>
    </div>
    """, unsafe_allow_html=True)

with nc3:
    st.markdown("""
    <div class="nav-card">
        <h3 style='color: #0d6efd; margin-top: 0;'>👥 Comparison</h3>
        <p style='color: #6c757d; margin-bottom: 0;'>Compare across demographics</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.success(f"✅ Data loaded • {len(df)} responses • {df.shape[1]} features • Auto-refresh enabled")

with st.expander("ℹ️ About"):
    st.markdown("""
    **UMK Sleep & Academic Performance Dashboard**
    
    Comprehensive analysis of sleep quality impact on academic outcomes among 
    Universiti Malaysia Kelantan students with real-time data synchronization.
    """)
