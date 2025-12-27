import streamlit as st
from data_loader import get_dataframe_from_session

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    h1 {
        color: #ffffff !important;
        font-size: 3rem !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .stCaption {
        color: #f0f0f0 !important;
        font-size: 1.1rem !important;
    }
    
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
    
    .metric-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        color: #667eea;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: #718096;
        font-size: 1rem;
        margin: 0;
    }
    
    .info-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .info-card h3 {
        color: #667eea !important;
        margin-bottom: 1rem !important;
    }
    
    [data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏠 Home Dashboard")
st.caption("📊 Overview of your dataset and key performance metrics")

df = get_dataframe_from_session()
if df is None:
    st.markdown("""
    <div class="info-card">
        <h3>⚠️ No Data Available</h3>
        <p>Please go back to the main page and load your data first.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Key metrics in beautiful cards
st.markdown("### 📊 Key Metrics Overview")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">📝</div>
        <div class="metric-value">{len(df)}</div>
        <div class="metric-label">Total Responses</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    if "InsomniaSeverity_index" in df.columns:
        mean_val = df['InsomniaSeverity_index'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">😴</div>
            <div class="metric-value">{mean_val:.2f}</div>
            <div class="metric-label">Mean Insomnia Severity</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">😴</div>
            <div class="metric-value">N/A</div>
            <div class="metric-label">Mean Insomnia Severity</div>
        </div>
        """, unsafe_allow_html=True)

with c3:
    if "AcademicImpact_index" in df.columns:
        mean_val = df['AcademicImpact_index'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🎓</div>
            <div class="metric-value">{mean_val:.2f}</div>
            <div class="metric-label">Mean Academic Impact</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">🎓</div>
            <div class="metric-value">N/A</div>
            <div class="metric-label">Mean Academic Impact</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Additional metrics
c4, c5, c6 = st.columns(3)

with c4:
    if "SleepHours_est" in df.columns:
        mean_sleep = df['SleepHours_est'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">⏰</div>
            <div class="metric-value">{mean_sleep:.1f}h</div>
            <div class="metric-label">Average Sleep Duration</div>
        </div>
        """, unsafe_allow_html=True)

with c5:
    if "SleepQuality_score" in df.columns:
        mean_quality = df['SleepQuality_score'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">⭐</div>
            <div class="metric-value">{mean_quality:.2f}/5</div>
            <div class="metric-label">Average Sleep Quality</div>
        </div>
        """, unsafe_allow_html=True)

with c6:
    if "Stress_score" in df.columns:
        mean_stress = df['Stress_score'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">😰</div>
            <div class="metric-value">{mean_stress:.2f}/4</div>
            <div class="metric-label">Average Stress Level</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Dataset information
st.markdown("### 📋 Dataset Information")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown(f"""
    <div class="info-card">
        <h3>📊 Dataset Dimensions</h3>
        <p><strong>Rows:</strong> {len(df):,}</p>
        <p><strong>Columns:</strong> {df.shape[1]}</p>
        <p><strong>Missing Values:</strong> {df.isnull().sum().sum():,}</p>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    # Calculate some quick stats
    demographic_cols = [col for col in df.columns if any(x in col.lower() for x in ['gender', 'age', 'year', 'faculty'])]
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    st.markdown(f"""
    <div class="info-card">
        <h3>🔢 Column Types</h3>
        <p><strong>Demographic Fields:</strong> {len(demographic_cols)}</p>
        <p><strong>Numeric Metrics:</strong> {len(numeric_cols)}</p>
        <p><strong>Total Features:</strong> {df.shape[1]}</p>
    </div>
    """, unsafe_allow_html=True)

# Data preview
st.markdown("### 👀 Data Preview")
st.markdown("""
<div style='background: rgba(255,255,255,0.95); border-radius: 15px; padding: 1.5rem; box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
""", unsafe_allow_html=True)

st.dataframe(df.head(30), use_container_width=True, height=400)

st.markdown("</div>", unsafe_allow_html=True)

# Navigation tip
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="info-card">
    <h3>💡 Next Steps</h3>
    <p>Navigate to other pages using the sidebar:</p>
    <ul>
        <li><strong>Insomnia Visualisation</strong> - View comprehensive charts and analysis</li>
        <li><strong>Subgroup Comparison</strong> - Compare different student demographics</li>
    </ul>
</div>
""", unsafe_allow_html=True)
