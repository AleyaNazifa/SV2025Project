import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="UMK Insomnia & Education Survey",
    page_icon="😴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful sidebar and overall styling
st.markdown("""
    <style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: white;
    }
    
    /* Sidebar text color */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    /* Main content area */
    .main {
        background-color: #f8fafc;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
        color: #1e40af;
    }
    
    /* Headers */
    h1 {
        color: #1e3a8a;
        font-weight: 700;
        padding-bottom: 1rem;
        border-bottom: 3px solid #3b82f6;
    }
    
    h2, h3 {
        color: #1e40af;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
    }
    </style>
""", unsafe_allow_html=True)

# Google Sheets CSV URL
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSf4umx6QNDel99If8P2otizAHj7jEDxFIsqandbD0zYVzfDheZo2YVkK1_zknpDKjHnBuYWCINgcCe/pub?output=csv"

# Load data with caching
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load the data
df = load_data()

# Sidebar with beautiful styling
with st.sidebar:
    st.markdown("# 📊 Dashboard")
    st.markdown("### Insomnia & Education Survey")
    st.markdown("---")
    
    if df is not None:
        # Display metrics in sidebar
        st.markdown("### 📈 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total", len(df), label_visibility="visible")
        with col2:
            st.metric("Fields", len(df.columns), label_visibility="visible")
        
        st.markdown("---")
        
        # Last updated info
        st.markdown("### ⏰ Data Status")
        st.info(f"🕐 Updated: {datetime.now().strftime('%H:%M:%S')}\n\n📅 {datetime.now().strftime('%d %B %Y')}")
        
        # Refresh button
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Navigation instructions
        st.markdown("### 🧭 Navigation")
        st.markdown("""
        Use the sidebar menu above to navigate between:
        - 🏠 **Home** (Overview)
        - 👤 **Member 1** Analysis
        - 👤 **Member 2** Analysis  
        - 👤 **Member 3** Analysis
        """)
    
    st.markdown("---")
    st.markdown("### 🎓 UMK Research")
    st.markdown("*Faculty of Data Science & Computing*")

# Main content
st.title("😴 Insomnia and Educational Outcomes Survey")
st.markdown("### UMK Students Research Dashboard")
st.markdown("---")

if df is not None:
    # Hero section with metrics
    st.markdown("## 📊 Survey Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📝 Total Responses",
            value=len(df),
            delta="Live Data"
        )
    
    with col2:
        st.metric(
            label="❓ Survey Questions",
            value=len(df.columns),
            delta=None
        )
    
    with col3:
        faculty_count = df['Which faculty are you currently enrolled in?'].nunique()
        st.metric(
            label="🏛️ Faculties",
            value=faculty_count,
            delta=None
        )
    
    with col4:
        st.metric(
            label="📊 Status",
            value="✅ Active",
            delta=None
        )
    
    st.markdown("---")
    
    # About section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🎯 Research Objectives")
        st.markdown("""
        This dashboard presents comprehensive analysis of insomnia patterns and their impact on 
        educational outcomes among UMK students. The study examines:
        
        - **Sleep Patterns**: Duration, quality, and disturbances
        - **Academic Performance**: GPA, concentration, and attendance
        - **Lifestyle Factors**: Device usage, caffeine consumption, and exercise habits
        - **Health Impact**: Stress levels and overall wellbeing
        """)
    
    with col2:
        st.markdown("## 👥 Research Team")
        st.info("""
        **Member 1**: Demographics & Sleep Patterns
        
        **Member 2**: Academic Performance Analysis
        
        **Member 3**: Lifestyle & Health Factors
        """)
    
    st.markdown("---")
    
    # Data preview section
    st.markdown("## 📋 Survey Data Preview")
    
    # Expandable section for full data
    with st.expander("👀 Click to view full dataset", expanded=False):
        st.dataframe(df, use_container_width=True, height=400)
    
    # Column information
    with st.expander("📑 Survey Questions/Columns", expanded=False):
        for i, col in enumerate(df.columns, 1):
            st.markdown(f"**{i}.** {col}")
    
    st.markdown("---")
    
    # Download section
    st.markdown("## ⬇️ Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"umk_insomnia_survey_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        st.download_button(
            label="📊 Download as Excel",
            data=csv,  # You could convert to Excel format here
            file_name=f"umk_insomnia_survey_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        st.button("📧 Share Report", use_container_width=True, disabled=True)
    
    st.markdown("---")
    
    # Instructions
    st.markdown("## 🚀 Getting Started")
    st.success("""
    **To explore the analysis:**
    1. Use the **sidebar menu** to navigate between different team member analyses
    2. Each page contains **5 unique visualizations** 
    3. Data **automatically updates** every 5 minutes from Google Sheets
    4. Click **Refresh Data** in the sidebar for manual updates
    """)
    
else:
    st.error("❌ Unable to load data. Please check your Google Sheets link.")
    st.info("""
    **Troubleshooting Steps:**
    1. Ensure your Google Sheet is published to the web
    2. Go to File → Share → Publish to web
    3. Select 'Entire Document' and 'CSV' format
    4. Update the CSV_URL in the code with your link
    """)
