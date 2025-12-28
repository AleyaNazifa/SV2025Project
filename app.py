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

# Custom CSS for professional styling
st.markdown("""
    <style>
    /* Sidebar styling - Professional dark purple/indigo */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4c1d95 0%, #5b21b6 50%, #6d28d9 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Sidebar header */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #fbbf24 !important;
        font-weight: 700 !important;
    }
    
    /* Main content area */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: bold;
        color: #5b21b6;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: #4c1d95;
        font-weight: 600;
    }
    
    /* Headers */
    h1 {
        color: #4c1d95;
        font-weight: 800;
        padding-bottom: 1rem;
        border-bottom: 4px solid #8b5cf6;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: #5b21b6;
        font-weight: 700;
    }
    
    h3 {
        color: #6d28d9;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #ede9fe;
        border-left: 5px solid #8b5cf6;
        border-radius: 8px;
    }
    
    /* Navigation cards */
    .nav-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #8b5cf6;
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
@st.cache_data(ttl=300)  # Cache for 5 minutes
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

# Sidebar with professional styling
with st.sidebar:
    st.markdown("# 📊 Dashboard")
    st.markdown("### Insomnia & Education Survey")
    st.markdown("---")
    
    if df is not None:
        # Display metrics in sidebar
        st.markdown("### 📈 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📝 Responses", len(df))
        with col2:
            st.metric("❓ Questions", len(df.columns))
        
        st.markdown("---")
        
        # Last updated info with Malaysian time
        st.markdown("### ⏰ Data Status")
        my_time = get_malaysian_time()
        st.info(f"""
        🕐 **Last Updated**  
        {my_time.strftime('%H:%M:%S')} MYT
        
        📅 **Date**  
        {my_time.strftime('%d %B %Y')}
        """)
        
        # Refresh button
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Quick navigation to pages
        st.markdown("### 🧭 Quick Navigation")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("👤\n\nM1", use_container_width=True, help="Member 1 Analysis"):
                st.switch_page("pages/1_👤_Member_1_Analysis.py")
        
        with col2:
            if st.button("👤\n\nM2", use_container_width=True, help="Member 2 Analysis"):
                st.switch_page("pages/2_👤_Member_2_Analysis.py")
        
        with col3:
            if st.button("👤\n\nM3", use_container_width=True, help="Member 3 Analysis"):
                st.switch_page("pages/3_👤_Member_3_Analysis.py")
        
        st.markdown("---")
        
        st.markdown("""
        **💡 Tips:**
        - Use sidebar menu above for detailed analysis
        - Click quick buttons for fast navigation
        - Data updates automatically every 5 minutes
        """)
    
    st.markdown("---")
    st.markdown("### 🎓 UMK Research")
    st.markdown("*Faculty of Data Science & Computing*")
    st.markdown("*© 2025 - All Rights Reserved*")

# Main content
st.title("😴 Insomnia and Educational Outcomes Survey")
st.markdown("### 🎓 UMK Students Research Dashboard")
st.markdown("---")

if df is not None:
    # Hero section with metrics
    st.markdown("## 📊 Survey Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📝 Total Responses",
            value=len(df),
            delta="Live Data",
            delta_color="normal"
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
            delta="Real-time",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # Quick access navigation cards
    st.markdown("## 🚀 Quick Access to Team Analysis")
    
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
            st.switch_page("pages/1_👤_Member_1_Analysis.py")
    
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
            st.switch_page("pages/2_👤_Member_2_Analysis.py")
    
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
            st.switch_page("pages/3_👤_Member_3_Analysis.py")
    
    st.markdown("---")
    
    # About section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🎯 Research Objectives")
        st.markdown("""
        This comprehensive dashboard presents an in-depth analysis of insomnia patterns and their 
        impact on educational outcomes among Universiti Malaysia Kelantan (UMK) students.
        
        **Key Research Areas:**
        - **Sleep Patterns**: Duration, quality, disturbances, and bedtime habits
        - **Academic Performance**: GPA correlation, concentration levels, and attendance
        - **Lifestyle Factors**: Device usage, caffeine intake, and exercise habits
        - **Health Impact**: Stress levels, fatigue, and overall wellbeing assessment
        
        Our research aims to identify actionable insights to improve student health and academic success.
        """)
    
    with col2:
        st.markdown("## 👥 Research Team")
        st.info("""
        **👤 Member 1**  
        *Demographics & Sleep Patterns*
        
        **👤 Member 2**  
        *Academic Performance Analysis*
        
        **👤 Member 3**  
        *Lifestyle & Health Factors*
        
        ---
        
        **🏛️ Institution**  
        Universiti Malaysia Kelantan
        
        **📚 Faculty**  
        Data Science & Computing
        """)
    
    st.markdown("---")
    
    # Data preview section
    st.markdown("## 📋 Survey Data Preview")
    
    # Tabs for better organization
    tab1, tab2, tab3 = st.tabs(["📊 Data View", "📑 Column Info", "📈 Statistics"])
    
    with tab1:
        st.dataframe(df, use_container_width=True, height=400)
    
    with tab2:
        st.markdown("### Survey Questions")
        for i, col in enumerate(df.columns, 1):
            st.markdown(f"**{i}.** {col}")
    
    with tab3:
        st.markdown("### Dataset Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", len(df))
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            st.metric("Complete Responses", len(df.dropna()))
    
    st.markdown("---")
    
    # Download section
    st.markdown("## ⬇️ Export Data")
    
    col1, col2, col3, col4 = st.columns(4)
    
    my_time = get_malaysian_time()
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"umk_insomnia_survey_{my_time.strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        st.download_button(
            label="📊 Export Excel",
            data=csv,
            file_name=f"umk_insomnia_survey_{my_time.strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        if st.button("📧 Share Report", use_container_width=True):
            st.info("Feature coming soon!")
    
    with col4:
        if st.button("📄 Print View", use_container_width=True):
            st.info("Use browser's print function (Ctrl+P)")
    
    st.markdown("---")
    
    # Instructions
    st.markdown("## 🚀 Getting Started Guide")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **📖 How to Navigate:**
        1. Use **sidebar menu** or **quick buttons** above
        2. Each member page contains **5 detailed visualizations**
        3. Data updates **automatically every 5 minutes**
        4. Click **Refresh Data** for manual updates
        5. Export data using download buttons below
        """)
    
    with col2:
        st.info("""
        **💡 Features:**
        - ✅ Real-time data from Google Sheets
        - ✅ Interactive visualizations with Plotly
        - ✅ Professional statistical analysis
        - ✅ Mobile-responsive design
        - ✅ Export and share capabilities
        """)
    
else:
    st.error("❌ Unable to load data. Please check your Google Sheets connection.")
    st.info("""
    **🔧 Troubleshooting Steps:**
    1. Verify Google Sheet is published to web
    2. Go to **File → Share → Publish to web**
    3. Select **'Entire Document'** and **'CSV'** format
    4. Click **'Publish'** and update CSV_URL in code
    5. Try refreshing the page
    """)
