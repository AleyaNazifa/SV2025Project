import streamlit as st
from data_loader import (
    load_from_url,
    load_from_upload,
    ensure_engineered_columns,
    set_dataframe_in_session,
)

# Page config
st.set_page_config(
    page_title="UMK Sleep & Academic Dashboard", 
    layout="wide",
    page_icon="🌙",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clean Professional Style
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        background-color: #f7fafc;
        font-family: 'Inter', sans-serif;
    }
    
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }
    
    /* Headers */
    h1 {
        color: #1a202c !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: #2d3748 !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        color: #4a5568 !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] h2 {
        color: #2d3748 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #4299e1;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #3182ce;
        box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        font-weight: 500;
        color: #718096;
    }
    
    /* Custom cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.2s;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .objective-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        margin: 2rem 0;
    }
    
    .summary-box {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    
    .icon-badge {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #4299e1;
    }
    
    /* Input fields */
    .stTextInput input {
        border-radius: 8px;
        border: 1px solid #cbd5e0;
    }
    
    /* Radio buttons */
    .stRadio > label {
        font-weight: 500;
        color: #4a5568;
    }
    
    /* Section divider */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("---")

mode = st.sidebar.radio(
    "Data Source",
    ["🌐 Live Google Sheet", "📁 Upload CSV"],
    index=0
)

if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")

# Data loading
if mode == "🌐 Live Google Sheet":
    st.sidebar.markdown("**Google Sheet URL**")
    st.sidebar.caption("Enter your published CSV URL")
    
    csv_url = st.sidebar.text_input(
        "CSV URL",
        value="",
        placeholder="https://docs.google.com/.../pub?output=csv",
        label_visibility="collapsed"
    )
    
    if not csv_url.strip():
        # Welcome screen
        st.markdown("# 🌙 UMK Insomnia & Educational Outcomes Dashboard")
        st.markdown("### Multi-page application for sleep quality and academic performance analysis")
        st.markdown("---")
        
        st.info("👈 **Enter your Google Sheet CSV URL in the sidebar to begin**")
        
        with st.expander("📖 How to get your CSV URL"):
            st.markdown("""
            1. Open your Google Sheet
            2. Go to **File** → **Share** → **Publish to web**
            3. Select **Comma-separated values (.csv)** format
            4. Copy the URL and paste it in the sidebar
            5. Click outside the input box to load data
            """)
        
        with st.expander("📊 Expected Data Format"):
            st.markdown("""
            Your CSV should contain columns for:
            - Sleep quality measurements
            - Academic performance metrics
            - Student demographics (age, gender, faculty, year)
            - Lifestyle factors (exercise, caffeine, device use)
            """)
        
        st.stop()
    
    with st.spinner("📥 Loading data from Google Sheet..."):
        df = load_from_url(csv_url.strip())
        
else:
    uploaded = st.sidebar.file_uploader(
        "Upload CSV File",
        type=["csv"],
        help="Upload your sleep study data"
    )
    
    if uploaded is None:
        st.markdown("# 🌙 UMK Insomnia & Educational Outcomes Dashboard")
        st.markdown("### Multi-page application for sleep quality and academic performance analysis")
        st.markdown("---")
        
        st.info("👈 **Upload your CSV file in the sidebar to begin**")
        st.stop()
    
    with st.spinner("📥 Processing CSV file..."):
        df = load_from_upload(uploaded)

# Process data
df = ensure_engineered_columns(df)
set_dataframe_in_session(df)

# Main dashboard
st.markdown("# 🌙 UMK Sleep & Academic Study Dashboard")
st.markdown("### Research on Sleep Quality and Academic Performance (2024)")
st.markdown("---")

# Objective Statement
st.markdown("""
<div class="objective-card">
    <h2 style='color: #2d3748; margin-top: 0;'>🎯 Research Objective</h2>
    <p style='color: #4a5568; font-size: 1.05rem; line-height: 1.7; margin-bottom: 0;'>
        Analyze the <strong>relationship between sleep quality and academic performance</strong> among UMK students 
        to identify correlations between insomnia severity, sleep patterns, lifestyle factors, and educational outcomes.
    </p>
</div>
""", unsafe_allow_html=True)

# Summary Statistics
st.markdown("## 📊 Summary Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="summary-box">
        <div class="icon-badge">📝</div>
        <div style='font-size: 2.5rem; font-weight: 700; color: #2d3748; margin: 0.5rem 0;'>{}</div>
        <div style='font-size: 0.875rem; color: #718096; font-weight: 500;'>Total Responses</div>
    </div>
    """.format(len(df)), unsafe_allow_html=True)

with col2:
    if "InsomniaSeverity_index" in df.columns:
        avg_val = df['InsomniaSeverity_index'].mean()
        st.markdown("""
        <div class="summary-box">
            <div class="icon-badge">😴</div>
            <div style='font-size: 2.5rem; font-weight: 700; color: #2d3748; margin: 0.5rem 0;'>{:.2f}</div>
            <div style='font-size: 0.875rem; color: #718096; font-weight: 500;'>Avg Insomnia Severity</div>
            <div style='font-size: 0.75rem; color: #a0aec0; margin-top: 0.25rem;'>(Scale: 0-4)</div>
        </div>
        """.format(avg_val), unsafe_allow_html=True)

with col3:
    if "AcademicImpact_index" in df.columns:
        avg_val = df['AcademicImpact_index'].mean()
        st.markdown("""
        <div class="summary-box">
            <div class="icon-badge">🎓</div>
            <div style='font-size: 2.5rem; font-weight: 700; color: #2d3748; margin: 0.5rem 0;'>{:.2f}</div>
            <div style='font-size: 0.875rem; color: #718096; font-weight: 500;'>Avg Academic Impact</div>
            <div style='font-size: 0.75rem; color: #a0aec0; margin-top: 0.25rem;'>(Scale: 0-4)</div>
        </div>
        """.format(avg_val), unsafe_allow_html=True)

with col4:
    if "SleepHours_est" in df.columns:
        avg_val = df['SleepHours_est'].mean()
        st.markdown("""
        <div class="summary-box">
            <div class="icon-badge">⏰</div>
            <div style='font-size: 2.5rem; font-weight: 700; color: #2d3748; margin: 0.5rem 0;'>{:.1f}h</div>
            <div style='font-size: 0.875rem; color: #718096; font-weight: 500;'>Avg Sleep Duration</div>
            <div style='font-size: 0.75rem; color: #a0aec0; margin-top: 0.25rem;'>Per night</div>
        </div>
        """.format(avg_val), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Additional metrics
col5, col6, col7 = st.columns(3)

with col5:
    if "SleepQuality_score" in df.columns:
        avg_val = df['SleepQuality_score'].mean()
        st.metric(
            label="⭐ Average Sleep Quality",
            value=f"{avg_val:.2f} / 5",
            delta=None
        )

with col6:
    if "Stress_score" in df.columns:
        avg_val = df['Stress_score'].mean()
        st.metric(
            label="😰 Average Stress Level",
            value=f"{avg_val:.2f} / 4",
            delta=None
        )

with col7:
    if "AcademicPerformance_score" in df.columns:
        avg_val = df['AcademicPerformance_score'].mean()
        st.metric(
            label="📚 Average Academic Performance",
            value=f"{avg_val:.2f} / 5",
            delta=None
        )

st.markdown("---")

# Navigation guide
st.markdown("## 🧭 Navigation")
st.markdown("Use the sidebar menu to explore different analysis sections:")

nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    st.markdown("""
    <div class="metric-card">
        <h3 style='color: #2d3748; margin-top: 0;'>🏠 Home</h3>
        <p style='color: #718096; margin-bottom: 0;'>Overview and dataset summary with detailed metrics and statistics</p>
    </div>
    """, unsafe_allow_html=True)

with nav_col2:
    st.markdown("""
    <div class="metric-card">
        <h3 style='color: #2d3748; margin-top: 0;'>📈 Insomnia Visualisation</h3>
        <p style='color: #718096; margin-bottom: 0;'>Five comprehensive scientific visualizations and analysis</p>
    </div>
    """, unsafe_allow_html=True)

with nav_col3:
    st.markdown("""
    <div class="metric-card">
        <h3 style='color: #2d3748; margin-top: 0;'>👥 Subgroup Comparison</h3>
        <p style='color: #718096; margin-bottom: 0;'>Compare metrics across different student demographics</p>
    </div>
    """, unsafe_allow_html=True)

# Data status
st.markdown("---")
st.success(f"✅ **Data successfully loaded and processed** • {len(df)} responses • {df.shape[1]} columns • Auto-refresh enabled")

# Footer info
with st.expander("ℹ️ About this Dashboard"):
    st.markdown("""
    **UMK Insomnia & Educational Outcomes Dashboard**
    
    This dashboard provides comprehensive analysis of sleep quality and its impact on academic performance among 
    Universiti Malaysia Kelantan students. The data is automatically updated from Google Sheets.
    
    **Features:**
    - Real-time data synchronization
    - Interactive visualizations
    - Statistical analysis
    - Demographic comparisons
    - Correlation analysis
    """)
