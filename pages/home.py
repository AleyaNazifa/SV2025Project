import streamlit as st
from data_loader import get_dataframe_from_session

st.title("🏠 Home Dashboard")
st.markdown("### Comprehensive overview of sleep study data")
st.divider()

df = get_dataframe_from_session()
if df is None:
    st.warning("⚠️ No data available. Load data from the main page first.")
    st.stop()

# Key Metrics
st.markdown("## 📊 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📝 Total Responses", f"{len(df):,}")

with col2:
    if "InsomniaSeverity_index" in df.columns:
        st.metric("😴 Avg Insomnia", f"{df['InsomniaSeverity_index'].mean():.2f}")
    else:
        st.metric("😴 Avg Insomnia", "N/A")

with col3:
    if "AcademicImpact_index" in df.columns:
        st.metric("🎓 Avg Impact", f"{df['AcademicImpact_index'].mean():.2f}")
    else:
        st.metric("🎓 Avg Impact", "N/A")

st.markdown("<br>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    if "SleepHours_est" in df.columns:
        st.metric("⏰ Sleep Duration", f"{df['SleepHours_est'].mean():.1f}h")

with col5:
    if "SleepQuality_score" in df.columns:
        st.metric("⭐ Sleep Quality", f"{df['SleepQuality_score'].mean():.2f}/5")

with col6:
    if "Stress_score" in df.columns:
        st.metric("😰 Stress Level", f"{df['Stress_score'].mean():.2f}/4")

st.divider()

# Dataset Info
st.markdown("## 📋 Dataset Information")

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.markdown(f"""
    **Dataset Dimensions:**
    - Total Rows: **{len(df):,}**
    - Total Columns: **{df.shape[1]}**
    - Missing Values: **{df.isnull().sum().sum():,}**
    - Completeness: **{100 * (1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1])):.1f}%**
    """)

with info_col2:
    demographic_cols = [col for col in df.columns if any(x in col.lower() for x in ['gender', 'age', 'year', 'faculty'])]
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    st.markdown(f"""
    **Column Breakdown:**
    - Demographic Fields: **{len(demographic_cols)}**
    - Numeric Metrics: **{len(numeric_cols)}**
    - Categorical Fields: **{len(df.select_dtypes(include=['object']).columns)}**
    - Total Features: **{df.shape[1]}**
    """)

st.divider()

# Demographics
st.markdown("## 👥 Sample Distribution")

dist_col1, dist_col2, dist_col3 = st.columns(3)

with dist_col1:
    gender_col = "What is your gender?"
    if gender_col in df.columns:
        st.markdown("**Gender Distribution:**")
        counts = df[gender_col].value_counts()
        for key, val in counts.items():
            pct = (val/len(df)*100)
            st.write(f"• {key}: **{val}** ({pct:.1f}%)")

with dist_col2:
    year_col = "What is your year of study?"
    if year_col in df.columns:
        st.markdown("**Year of Study:**")
        counts = df[year_col].value_counts().sort_index()
        for key, val in counts.items():
            pct = (val/len(df)*100)
            st.write(f"• {key}: **{val}** ({pct:.1f}%)")

with dist_col3:
    age_col = "What is your age group?"
    if age_col in df.columns:
        st.markdown("**Age Groups:**")
        counts = df[age_col].value_counts()
        for key, val in counts.items():
            pct = (val/len(df)*100)
            st.write(f"• {key}: **{val}** ({pct:.1f}%)")

st.divider()

# Data Preview
st.markdown("## 👀 Data Preview")
st.dataframe(df.head(50), use_container_width=True, height=400)

st.info("💡 Navigate to **Insomnia Visualisation** for charts or **Subgroup Comparison** for analysis")
