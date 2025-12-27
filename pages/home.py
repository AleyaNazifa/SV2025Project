import streamlit as st
from data_loader import get_dataframe_from_session

# Page styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        background-color: #f7fafc;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        color: #1a202c !important;
        font-weight: 600 !important;
    }
    
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
    
    .info-section {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        margin: 1.5rem 0;
    }
    
    [data-testid="stDataFrame"] {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏠 Home Dashboard")
st.markdown("### Comprehensive overview of sleep study data and key insights")
st.markdown("---")

df = get_dataframe_from_session()
if df is None:
    st.warning("⚠️ No data available. Please load data from the main page first.")
    st.stop()

# Key Metrics Section
st.markdown("## 📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div style='font-size: 2.5rem; text-align: center; margin-bottom: 0.5rem;'>📝</div>
        <div style='font-size: 2.5rem; font-weight: 700; color: #2d3748; text-align: center;'>{}</div>
        <div style='font-size: 0.875rem; color: #718096; font-weight: 500; text-align: center;'>Total Survey Responses</div>
    </div>
    """.format(len(df)), unsafe_allow_html=True)

with col2:
    if "InsomniaSeverity_index" in df.columns:
        mean_val = df['InsomniaSeverity_index'].mean()
        st.markdown("""
        <div class="metric-card">
            <div style='font-size: 2.5rem; text-align: center; margin-bottom: 0.5rem;'>😴</div>
            <div style='font-size: 2.5rem; font-weight: 700; color: #2d3748; text-align: center;'>{:.2f}</div>
            <div style='font-size: 0.875rem; color: #718096; font-weight: 500; text-align: center;'>Mean Insomnia Severity Index</div>
        </div>
        """.format(mean_val), unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="metric-card">
            <div style='font-size: 2.5rem; text-align: center; margin-bottom: 0.5rem;'>😴</div>
            <div style='font-size: 2.5rem; font-weight: 700; color: #a0aec0; text-align: center;'>N/A</div>
            <div style='font-size: 0.875rem; color: #718096; font-weight: 500; text-align: center;'>Mean Insomnia Severity Index</div>
        </div>
        """, unsafe_allow_html=True)

with col3:
    if "AcademicImpact_index" in df.columns:
        mean_val = df['AcademicImpact_index'].mean()
        st.markdown("""
        <div class="metric-card">
            <div style='font-size: 2.5rem; text-align: center; margin-bottom: 0.5rem;'>🎓</div>
            <div style='font-size: 2.5rem; font-weight: 700; color: #2d3748; text-align: center;'>{:.2f}</div>
            <div style='font-size: 0.875rem; color: #718096; font-weight: 500; text-align: center;'>Mean Academic Impact Index</div>
        </div>
        """.format(mean_val), unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="metric-card">
            <div style='font-size: 2.5rem; text-align: center; margin-bottom: 0.5rem;'>🎓</div>
            <div style='font-size: 2.5rem; font-weight: 700; color: #a0aec0; text-align: center;'>N/A</div>
            <div style='font-size: 0.875rem; color: #718096; font-weight: 500; text-align: center;'>Mean Academic Impact Index</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Additional Metrics
col4, col5, col6 = st.columns(3)

with col4:
    if "SleepHours_est" in df.columns:
        mean_sleep = df['SleepHours_est'].mean()
        st.metric("⏰ Average Sleep Duration", f"{mean_sleep:.1f} hours")

with col5:
    if "SleepQuality_score" in df.columns:
        mean_quality = df['SleepQuality_score'].mean()
        st.metric("⭐ Average Sleep Quality", f"{mean_quality:.2f} / 5")

with col6:
    if "Stress_score" in df.columns:
        mean_stress = df['Stress_score'].mean()
        st.metric("😰 Average Stress Level", f"{mean_stress:.2f} / 4")

st.markdown("---")

# Dataset Information
st.markdown("## 📋 Dataset Information")

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.markdown("""
    <div class="info-section">
        <h3 style='color: #2d3748; margin-top: 0;'>📊 Dataset Dimensions</h3>
        <table style='width: 100%; color: #4a5568;'>
            <tr><td><strong>Total Rows:</strong></td><td>{:,}</td></tr>
            <tr><td><strong>Total Columns:</strong></td><td>{}</td></tr>
            <tr><td><strong>Missing Values:</strong></td><td>{:,}</td></tr>
            <tr><td><strong>Completeness:</strong></td><td>{:.1f}%</td></tr>
        </table>
    </div>
    """.format(
        len(df),
        df.shape[1],
        df.isnull().sum().sum(),
        100 * (1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1]))
    ), unsafe_allow_html=True)

with info_col2:
    demographic_cols = [col for col in df.columns if any(x in col.lower() for x in ['gender', 'age', 'year', 'faculty'])]
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    st.markdown("""
    <div class="info-section">
        <h3 style='color: #2d3748; margin-top: 0;'>🔢 Column Breakdown</h3>
        <table style='width: 100%; color: #4a5568;'>
            <tr><td><strong>Demographic Fields:</strong></td><td>{}</td></tr>
            <tr><td><strong>Numeric Metrics:</strong></td><td>{}</td></tr>
            <tr><td><strong>Categorical Fields:</strong></td><td>{}</td></tr>
            <tr><td><strong>Total Features:</strong></td><td>{}</td></tr>
        </table>
    </div>
    """.format(
        len(demographic_cols),
        len(numeric_cols),
        len(df.select_dtypes(include=['object']).columns),
        df.shape[1]
    ), unsafe_allow_html=True)

st.markdown("---")

# Data Distribution by Demographics
st.markdown("## 👥 Sample Distribution")

dist_col1, dist_col2, dist_col3 = st.columns(3)

with dist_col1:
    gender_col = "What is your gender?"
    if gender_col in df.columns:
        counts = df[gender_col].value_counts()
        st.markdown("**Gender Distribution**")
        for idx, (key, val) in enumerate(counts.items()):
            pct = (val/len(df)*100)
            st.metric(f"{key}", f"{val} ({pct:.1f}%)", label_visibility="visible")

with dist_col2:
    year_col = "What is your year of study?"
    if year_col in df.columns:
        counts = df[year_col].value_counts().sort_index()
        st.markdown("**Year of Study**")
        for idx, (key, val) in enumerate(counts.items()):
            pct = (val/len(df)*100)
            st.metric(f"{key}", f"{val} ({pct:.1f}%)", label_visibility="visible")

with dist_col3:
    age_col = "What is your age group?"
    if age_col in df.columns:
        counts = df[age_col].value_counts()
        st.markdown("**Age Groups**")
        for idx, (key, val) in enumerate(counts.items()):
            pct = (val/len(df)*100)
            st.metric(f"{key}", f"{val} ({pct:.1f}%)", label_visibility="visible")

st.markdown("---")

# Data Preview
st.markdown("## 👀 Data Preview")
st.dataframe(
    df.head(50), 
    use_container_width=True, 
    height=400
)

# Next Steps
st.markdown("---")
st.info("💡 **Next Steps:** Navigate to **Insomnia Visualisation** for detailed charts or **Subgroup Comparison** for demographic analysis")
