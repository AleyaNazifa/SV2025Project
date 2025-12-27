import streamlit as st
from data_loader import (
    load_from_url,
    load_from_upload,
    ensure_engineered_columns,
    set_dataframe_in_session,
)

# Page config with custom theme
st.set_page_config(
    page_title="UMK Sleep & Academic Dashboard", 
    layout="wide",
    page_icon="🌙",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
    <style>
    /* Main content styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Card styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Title styling */
    h1 {
        color: #ffffff !important;
        font-size: 3rem !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem !important;
    }
    
    /* Subtitle styling */
    .stCaption {
        color: #f0f0f0 !important;
        font-size: 1.1rem !important;
        margin-bottom: 2rem !important;
    }
    
    /* Info box styling */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2) !important;
    }
    
    /* Success box styling */
    .stSuccess {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2) !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Radio button styling */
    .stRadio > label {
        font-weight: 600 !important;
        color: #ffffff !important;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #667eea;
        padding: 0.75rem;
    }
    
    /* Recommendations card */
    .recommendation-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .recommendation-card h3 {
        color: #667eea !important;
        margin-bottom: 1rem !important;
    }
    
    .recommendation-card ul {
        color: #2d3748;
    }
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header with emoji
st.title("🌙 UMK Insomnia & Educational Outcomes")
st.caption("📊 Multi-page Streamlit application for sleep quality and academic performance analysis")

# Sidebar configuration
st.sidebar.markdown("### 🔧 Data Source Configuration")
mode = st.sidebar.radio("Select data source mode", ["🌐 Live Google Sheet (Auto)", "📁 Upload CSV"], index=0)

refresh = st.sidebar.button("🔄 Refresh Data Now")
if refresh:
    st.cache_data.clear()
    st.rerun()

# Data loading logic
if mode == "🌐 Live Google Sheet (Auto)":
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📝 Example URL:**")
    st.sidebar.code("https://docs.google.com/.../pub?output=csv", language="text")
    
    csv_url = st.sidebar.text_input("Google Sheet CSV URL", value="", placeholder="Paste your CSV URL here...")
    
    if not csv_url.strip():
        st.markdown("""
        <div class="recommendation-card">
            <h3>👋 Welcome to the UMK Sleep Dashboard!</h3>
            <p>To get started, please enter your Google Sheet CSV URL in the sidebar.</p>
            <br>
            <p><strong>How to get your CSV URL:</strong></p>
            <ul>
                <li>Open your Google Sheet</li>
                <li>Go to File → Share → Publish to web</li>
                <li>Select "Comma-separated values (.csv)" format</li>
                <li>Copy the URL and paste it in the sidebar</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    with st.spinner("📥 Loading data from Google Sheet..."):
        df = load_from_url(csv_url.strip())
else:
    uploaded = st.sidebar.file_uploader("📤 Upload your CSV file", type=["csv"])
    
    if uploaded is None:
        st.markdown("""
        <div class="recommendation-card">
            <h3>👋 Welcome to the UMK Sleep Dashboard!</h3>
            <p>Please upload your CSV file using the sidebar to begin your analysis.</p>
            <br>
            <p><strong>Your CSV should contain:</strong></p>
            <ul>
                <li>Sleep quality measurements</li>
                <li>Academic performance data</li>
                <li>Student demographic information</li>
                <li>Lifestyle factors (exercise, caffeine, etc.)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    with st.spinner("📥 Processing your CSV file..."):
        df = load_from_upload(uploaded)

# Process data
df = ensure_engineered_columns(df)
set_dataframe_in_session(df)

# Success message with metrics
st.success(f"✅ Data loaded successfully! **{len(df)}** responses • **{df.shape[1]}** columns analyzed")

# Quick stats in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='background: rgba(255,255,255,0.95); padding: 1.5rem; border-radius: 15px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
        <h2 style='color: #667eea; margin: 0;'>📊</h2>
        <p style='color: #2d3748; font-size: 2rem; font-weight: bold; margin: 0.5rem 0;'>{}</p>
        <p style='color: #718096; margin: 0;'>Total Responses</p>
    </div>
    """.format(len(df)), unsafe_allow_html=True)

with col2:
    if "InsomniaSeverity_index" in df.columns:
        avg_insomnia = df['InsomniaSeverity_index'].mean()
        st.markdown("""
        <div style='background: rgba(255,255,255,0.95); padding: 1.5rem; border-radius: 15px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
            <h2 style='color: #764ba2; margin: 0;'>😴</h2>
            <p style='color: #2d3748; font-size: 2rem; font-weight: bold; margin: 0.5rem 0;'>{:.2f}</p>
            <p style='color: #718096; margin: 0;'>Avg Insomnia Severity</p>
        </div>
        """.format(avg_insomnia), unsafe_allow_html=True)

with col3:
    if "AcademicImpact_index" in df.columns:
        avg_impact = df['AcademicImpact_index'].mean()
        st.markdown("""
        <div style='background: rgba(255,255,255,0.95); padding: 1.5rem; border-radius: 15px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
            <h2 style='color: #667eea; margin: 0;'>🎓</h2>
            <p style='color: #2d3748; font-size: 2rem; font-weight: bold; margin: 0.5rem 0;'>{:.2f}</p>
            <p style='color: #718096; margin: 0;'>Avg Academic Impact</p>
        </div>
        """.format(avg_impact), unsafe_allow_html=True)

with col4:
    if "SleepHours_est" in df.columns:
        avg_sleep = df['SleepHours_est'].mean()
        st.markdown("""
        <div style='background: rgba(255,255,255,0.95); padding: 1.5rem; border-radius: 15px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
            <h2 style='color: #764ba2; margin: 0;'>⏰</h2>
            <p style='color: #2d3748; font-size: 2rem; font-weight: bold; margin: 0.5rem 0;'>{:.1f}h</p>
            <p style='color: #718096; margin: 0;'>Avg Sleep Duration</p>
        </div>
        """.format(avg_sleep), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Navigation guide
st.markdown("""
<div class="recommendation-card">
    <h3>🧭 Navigation Guide</h3>
    <p>Use the page navigation in the left sidebar to explore different sections:</p>
    <br>
    <ul>
        <li><strong>🏠 Home</strong> - Overview and dataset summary with key metrics</li>
        <li><strong>📈 Insomnia Visualisation</strong> - Five comprehensive scientific visualizations</li>
        <li><strong>👥 Subgroup Comparison</strong> - Compare different student groups (faculty, year, age)</li>
    </ul>
</div>
""", unsafe_allow_html=True)
