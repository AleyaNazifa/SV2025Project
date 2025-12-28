import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# Page configuration
st.set_page_config(
    page_title="UMK Insomnia & Education Survey",
    page_icon="😴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
        font-weight: 500 !important;
    }
    
    .main {
        background: #f8fafc;
    }
    
    h1 {
        color: #0f172a !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 1.75rem !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        color: #334155 !important;
        font-weight: 600 !important;
    }
    
    p, div, span, label {
        color: #475569 !important;
        font-size: 1rem !important;
    }
    
    .stMetricLabel {
        color: #64748b !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    .stMetricValue {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white !important;
        font-weight: 600 !important;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        font-size: 1rem !important;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .nav-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #0f172a;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .nav-card:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        transform: translateY(-4px);
    }
    </style>
""", unsafe_allow_html=True)

# Google Sheets CSV URL
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSf4umx6QNDel99If8P2otizAHj7jEDxFIsqandbD0zYVzfDheZo2YVkK1_zknpDKjHnBuYWCINgcCe/pub?output=csv"

# Load data with caching
@st.cache_data(ttl=300)
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Get Malaysian time
def get_malaysian_time():
    malaysia_tz = pytz.timezone('Asia/Kuala_Lumpur')
    return datetime.now(malaysia_tz)

# Load the data
df = load_data()

# Sidebar
with st.sidebar:
    st.markdown("# 📊 Dashboard")
    st.markdown("### Insomnia Survey")
    st.markdown("---")
    
    if df is not None:
        st.markdown("### 📈 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📝 Responses", len(df))
        with col2:
            st.metric("❓ Questions", len(df.columns))
        
        st.markdown("---")
        
        my_time = get_malaysian_time()
        st.markdown("### ⏰ Data Status")
        st.info(f"""
        🕐 **Last Updated**  
        {my_time.strftime('%H:%M:%S')} MYT
        
        📅 **Date**  
        {my_time.strftime('%d %B %Y')}
        """)
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        st.markdown("### 🧭 Quick Navigation")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("👤\n\nM1", use_container_width=True):
                st.switch_page("pages/AleyaAelyana.py")
        
        with col2:
            if st.button("👤\n\nM2", use_container_width=True):
                st.switch_page("pages/AleyaNazifa.py")
        
        with col3:
            if st.button("👤\n\nM3", use_container_width=True):
                st.switch_page("pages/Nash.py")
    
    st.markdown("---")
    st.markdown("### 🎓 UMK Research")
    st.markdown("*Faculty of Data Science*")
    st.markdown("*© 2025*")

# Main content
st.title("😴 Insomnia and Educational Outcomes Survey")
st.markdown("### 🎓 UMK Students Research Dashboard")
st.markdown("---")

if df is not None:
    st.markdown("## 📊 Survey Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Total Responses", len(df), "Live Data")
    
    with col2:
        st.metric("❓ Survey Questions", len(df.columns))
    
    with col3:
        faculty_count = df['Which faculty are you currently enrolled in?'].nunique()
        st.metric("🏛️ Faculties", faculty_count)
    
    with col4:
        st.metric("📊 Status", "✅ Active")
    
    st.markdown("---")
    
    st.markdown("## 🚀 Quick Access to Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="nav-card">
            <h3>👤 Member 1</h3>
            <h4>Demographics & Sleep Patterns</h4>
            <p>• Gender & Age Distribution<br>
            • Sleep Duration Analysis<br>
            • Insomnia Frequency<br>
            • Sleep Quality Ratings</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 View Member 1 Analysis", use_container_width=True, key="nav1"):
            st.switch_page("pages/AleyaAelyana.py")
    
    with col2:
        st.markdown("""
        <div class="nav-card">
            <h3>👤 Member 2</h3>
            <h4>Academic Performance Impact</h4>
            <p>• Faculty Distribution<br>
            • GPA Analysis<br>
            • Concentration Issues<br>
            • Assignment Deadlines</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 View Member 2 Analysis", use_container_width=True, key="nav2"):
            st.switch_page("pages/AleyaNazifa.py")
    
    with col3:
        st.markdown("""
        <div class="nav-card">
            <h3>👤 Member 3</h3>
            <h4>Lifestyle & Health Factors</h4>
            <p>• Device Usage Patterns<br>
            • Caffeine Consumption<br>
            • Physical Activity<br>
            • Stress & Sleep Methods</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 View Member 3 Analysis", use_container_width=True, key="nav3"):
            st.switch_page("pages/Nash.py")
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🎯 Research Objectives")
        st.markdown("""
        This dashboard presents comprehensive analysis of insomnia patterns and their 
        impact on educational outcomes among UMK students.
        
        **Key Research Areas:**
        - **Sleep Patterns**: Duration, quality, and disturbances
        - **Academic Performance**: GPA, concentration, attendance
        - **Lifestyle Factors**: Device usage, caffeine, exercise
        - **Health Impact**: Stress levels and wellbeing
        """)
    
    with col2:
        st.markdown("## 👥 Research Team")
        st.info("""
        **👤 AleyaAelyana**  
        Demographics & Sleep
        
        **👤 Aleya Nazifa**  
        Academic Performance
        
        **👤 Nash**  
        Lifestyle & Health
        
        ---
        
        **🏛️ UMK**  
        Data Science Faculty
        """)
    
    st.markdown("---")
    
    st.markdown("## 📋 Data Preview")
    
    tab1, tab2 = st.tabs(["📊 Data View", "📑 Column Info"])
    
    with tab1:
        st.dataframe(df, use_container_width=True, height=400)
    
    with tab2:
        st.markdown("### Survey Questions")
        for i, col in enumerate(df.columns, 1):
            st.markdown(f"**{i}.** {col}")
    
    st.markdown("---")
    
    st.markdown("## ⬇️ Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    my_time = get_malaysian_time()
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"umk_survey_{my_time.strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        if st.button("📊 Export Excel", use_container_width=True):
            st.info("Use CSV format for now")
    
    with col3:
        if st.button("📄 Print View", use_container_width=True):
            st.info("Use Ctrl+P to print")
    
    st.markdown("---")
    
    st.markdown("## 🚀 Getting Started")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **📖 How to Navigate:**
        1. Use sidebar menu or buttons above
        2. Each page has 5 visualizations
        3. Auto-updates every 5 minutes
        4. Click Refresh for manual update
        """)
    
    with col2:
        st.info("""
        **💡 Features:**
        - ✅ Real-time data
        - ✅ Interactive charts
        - ✅ Professional analysis
        - ✅ Export capabilities
        """)

else:
    st.error("❌ Unable to load data. Please check connection.")
