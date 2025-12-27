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
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Title styling - WHITE and VISIBLE */
    h1 {
        color: #ffffff !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Subtitle/Caption styling - WHITE */
    .stMarkdown p, [data-testid="stMarkdownContainer"] p {
        color: #f0f0f0 !important;
        font-size: 1.05rem !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    
    /* Info/Alert boxes - WHITE BACKGROUND for readability */
    .stAlert, [data-testid="stAlert"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2) !important;
        color: #2d3748 !important;
    }
    
    .stAlert p {
        color: #2d3748 !important;
        text-shadow: none !important;
    }
    
    /* Success box */
    [data-testid="stSuccess"], .stSuccess {
        background: rgba(72, 187, 120, 0.95) !important;
        color: white !important;
        border: none !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white !important;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(72, 187, 120, 0.4);
        font-family: 'Inter', sans-serif;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(72, 187, 120, 0.6);
        background: linear-gradient(135deg, #38a169 0%, #2f855a 100%);
    }
    
    /* Radio button styling */
    .stRadio > label {
        font-weight: 600 !important;
        color: #ffffff !important;
        font-size: 1.05rem !important;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #667eea;
        padding: 0.75rem;
        background: white;
    }
    
    .stTextInput > label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Code block in sidebar */
    [data-testid="stSidebar"] code {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #90cdf4 !important;
        padding: 0.5rem;
        border-radius: 5px;
        display: block;
        word-break: break-all;
    }
    
    /* Recommendation cards */
    .recommendation-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .recommendation-card h3 {
        color: #667eea !important;
        margin-bottom: 1rem !important;
        text-shadow: none !important;
    }
    
    .recommendation-card p, .recommendation-card ul, .recommendation-card li {
        color: #2d3748 !important;
        text-shadow: none !important;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
    }
    
    [data-testid="stFileUploader"] label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header with emoji
st.title("🌙 UMK Insomnia & Educational Outcomes")
st.markdown("**📊 Multi-page Streamlit application for sleep quality and academic performance analysis**")

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
    st.sidebar.markdown("**📝 Example URL format:**")
    st.sidebar.code("https://docs.google.com/.../pub?output=csv")
    
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

# Success message
st.success(f"✅ Data loaded successfully! **{len(df)}** responses • **{df.shape[1]}** columns analyzed")

# Quick stats in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='background: rgba(255,255,255,0.95); padding: 1.5rem; border-radius: 15px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
        <h2 style='color: #667eea; margin: 0; text-shadow: none;'>📊</h2>
        <p style='color: #2d3748; font-size: 2rem; font-weight: bold; margin: 0.5rem 0; text-shadow: none;'>{}</p>
        <p style='color: #718096; margin: 0; text-shadow: none;'>Total Responses</p>
    </div>
    """.format(len(df)), unsafe_allow_html=True)

with col2:
    if "InsomniaSeverity_index" in df.columns:
        avg_insomnia = df['InsomniaSeverity_index'].mean()
        st.markdown("""
        <div style='background: rgba(255,255,255,0.95); padding: 1.5rem; border-radius: 15px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
            <h2 style='color: #764ba2; margin: 0; text-shadow: none;'>😴</h2>
            <p style='color: #2d3748; font-size: 2rem; font-weight: bold; margin: 0.5rem 0; text-shadow: none;'>{:.2f}</p>
            <p style='color: #718096; margin: 0; text-shadow: none;'>Avg Insomnia Severity</p>
        </div>
        """.format(avg_insomnia), unsafe_allow_html=True)

with col3:
    if "AcademicImpact_index" in df.columns:
        avg_impact = df['AcademicImpact_index'].mean()
        st.markdown("""
        <div style='background: rgba(255,255,255,0.95); padding: 1.5rem; border-radius: 15px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
            <h2 style='color: #667eea; margin: 0; text-shadow: none;'>🎓</h2>
            <p style='color: #2d3748; font-size: 2rem; font-weight: bold; margin: 0.5rem 0; text-shadow: none;'>{:.2f}</p>
            <p style='color: #718096; margin: 0; text-shadow: none;'>Avg Academic Impact</p>
        </div>
        """.format(avg_impact), unsafe_allow_html=True)

with col4:
    if "SleepHours_est" in df.columns:
        avg_sleep = df['SleepHours_est'].mean()
        st.markdown("""
        <div style='background: rgba(255,255,255,0.95); padding: 1.5rem; border-radius: 15px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
            <h2 style='color: #764ba2; margin: 0; text-shadow: none;'>⏰</h2>
            <p style='color: #2d3748; font-size: 2rem; font-weight: bold; margin: 0.5rem 0; text-shadow: none;'>{:.1f}h</p>
            <p style='color: #718096; margin: 0; text-shadow: none;'>Avg Sleep Duration</p>
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
