import streamlit as st
import pandas as pd
from datetime import datetime

# Google Sheets published CSV URL
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSf4umx6QNDel99If8P2otizAHj7jEDxFIsqandbD0zYVzfDheZo2YVkK1_zknpDKjHnBuYWCINgcCe/pub?output=csv"

@st.cache_data(ttl=300)
def load_data():
    """Load data from Google Sheets with automatic refresh"""
    try:
        df = pd.read_csv(GOOGLE_SHEETS_URL)

        # ✅ Clean headers: strip + collapse multiple spaces
        df.columns = [str(c).strip() for c in df.columns]
        df.columns = [" ".join(c.split()) for c in df.columns]

        # ✅ Build mapping (also normalized)
        column_mapping = {
            "Timestamp": "Timestamp",
            "What is your gender?": "Gender",
            "What is your age group?": "AgeGroup",
            "What is your year of study?": "YearOfStudy",
            "Which faculty are you currently enrolled in?": "Faculty",
            "How often do you have difficulty falling asleep at night?": "DifficultyFallingAsleep",
            "On average, how many hours of sleep do you get on a typical day?": "SleepHours",
            "How often do you wake up during the night and have trouble falling back asleep?": "NightWakeups",
            "How would you rate the overall quality of your sleep?": "SleepQuality",
            "At what time do you usually go to bed on weekdays?": "BedTime",
            "Do you usually nap during the day?": "DayNap",
            "How often do you experience difficulty concentrating during lectures or studying due to lack of sleep?": "ConcentrationDifficulty",
            "How often do you feel fatigued during the day, affecting your ability to study or attend classes?": "DaytimeFatigue",
            "How often do you miss or skip classes due to sleep-related issues (e.g., insomnia, feeling tired)?": "MissedClasses",
            "How would you describe the impact of insufficient sleep on your ability to complete assignments and meet deadlines?": "AssignmentImpact",
            "During exam periods, how much does your sleep pattern change?": "ExamSleepChange",
            "How would you rate your overall academic performance (GPA or grades) in the past semester?": "AcademicPerformance",
            "What is your GPA range for the most recent semester?": "GPA",
            "What is your CGPA range for the most recent semester?": "CGPA",
            "How often do you use electronic devices (e.g., phone, computer) before going to sleep?": "DeviceUsage",
            "How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?": "CaffeineConsumption",
            "How often do you engage in physical activity or exercise?": "PhysicalActivity",
            "How would you describe your stress levels related to academic workload?": "StressLevel",
            "Do you use any methods to help you sleep?": "SleepMethods",
        }

        # ✅ Rename only keys that actually exist (prevents KeyError)
        column_mapping_clean = {" ".join(k.split()): v for k, v in column_mapping.items()}
        existing_map = {k: v for k, v in column_mapping_clean.items() if k in df.columns}
        df = df.rename(columns=existing_map)

        # Convert timestamp to datetime (safe)
        if "Timestamp" in df.columns:
            df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

        # ✅ Compute InsomniaSeverity_index only if needed cols exist
        required = {"DifficultyFallingAsleep", "SleepQuality", "NightWakeups"}
        if required.issubset(df.columns):
            df["InsomniaSeverity_index"] = calculate_insomnia_index(df)
        else:
            missing = sorted(list(required - set(df.columns)))
            st.warning(f"Cannot compute InsomniaSeverity_index. Missing columns: {missing}")
            st.info(f"Available columns: {df.columns.tolist()}")

        return df

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def calculate_insomnia_index(df):
    """Calculate a simple insomnia severity score based on key indicators"""
    score = 0
    
    # Difficulty falling asleep (0-4 scale)
    sleep_difficulty_map = {
        'Never': 0,
        'Rarely (1–2 times a week)': 1,
        'Sometimes (3–4 times a week)': 2,
        'Often (5–6 times a week)': 3,
        'Always (every night)': 4
    }
    score += df['DifficultyFallingAsleep'].map(sleep_difficulty_map).fillna(0)
    
    # Sleep quality (inverse, 0-4 scale)
    quality_map = {
        '1': 4, '2': 3, '3': 2, '4': 1, '5': 0
    }
    score += df['SleepQuality'].astype(str).map(quality_map).fillna(0)
    
    # Night wakeups (0-4 scale)
    score += df['NightWakeups'].map(sleep_difficulty_map).fillna(0)
    
    # Normalize to 0-28 scale (like standard ISI)
    return (score / 12 * 28).round(1)

def get_data_info(df):
    """Get summary information about the dataset"""
    if df is None:
        return None
    
    return {
        'total_responses': len(df),
        'last_updated': df['Timestamp'].max(),
        'date_range': f"{df['Timestamp'].min().strftime('%Y-%m-%d')} to {df['Timestamp'].max().strftime('%Y-%m-%d')}",
        'faculties': df['Faculty'].nunique(),
        'avg_isi': df['InsomniaSeverity_index'].mean()
    }

def display_sidebar_info():
    """Display beautiful sidebar with auto-refresh info"""
    st.sidebar.markdown("### 📊 Data Status")
    
    if 'data' not in st.session_state or st.session_state.data is None:
        st.session_state.data = load_data()
    
    df = st.session_state.data
    
    if df is not None:
        info = get_data_info(df)
        
        st.sidebar.success("✅ Data Loaded Successfully")
        st.sidebar.metric("Total Responses", info['total_responses'])
        st.sidebar.metric("Last Updated", 
                         info['last_updated'].strftime('%Y-%m-%d %H:%M'))
        st.sidebar.metric("Faculties", info['faculties'])
        st.sidebar.metric("Avg ISI Score", f"{info['avg_isi']:.1f}")
        
        st.sidebar.markdown("---")
        st.sidebar.caption(f"📅 Data Range: {info['date_range']}")
        st.sidebar.caption("🔄 Auto-refreshes every 5 minutes")
        
        # Manual refresh button
        if st.sidebar.button("🔄 Refresh Now", use_container_width=True):
            st.cache_data.clear()
            st.session_state.data = load_data()
            st.rerun()
    else:
        st.sidebar.error("❌ Failed to load data")
        if st.sidebar.button("🔄 Retry", use_container_width=True):
            st.cache_data.clear()
            st.session_state.data = load_data()
            st.rerun()

def get_df():
    """Get the current dataframe"""
    if 'data' not in st.session_state:
        st.session_state.data = load_data()
    return st.session_state.data
