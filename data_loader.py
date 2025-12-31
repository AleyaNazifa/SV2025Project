import streamlit as st
import pandas as pd

# Google Sheets published CSV URL
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSf4umx6QNDel99If8P2otizAHj7jEDxFIsqandbD0zYVzfDheZo2YVkK1_zknpDKjHnBuYWCINgcCe/pub?output=csv"


def _normalize_header(s: str) -> str:
    s = str(s).strip()
    s = " ".join(s.split())  # collapse multiple spaces
    return s


@st.cache_data(ttl=300)
def load_data():
    """Load data from Google Sheets with automatic refresh"""
    try:
        df = pd.read_csv(GOOGLE_SHEETS_URL)

        # ✅ CRITICAL: normalize headers to remove trailing spaces
        df.columns = [_normalize_header(c) for c in df.columns]

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

        # Normalize mapping keys too (same transformation)
        column_mapping = {_normalize_header(k): v for k, v in column_mapping.items()}

        # Rename only existing columns (prevents KeyError)
        existing_map = {k: v for k, v in column_mapping.items() if k in df.columns}
        df = df.rename(columns=existing_map)

        # Convert timestamp to datetime
        if "Timestamp" in df.columns:
            df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

        # Calculate Insomnia Severity Index (ISI)
        required = {"DifficultyFallingAsleep", "SleepQuality", "NightWakeups"}
        if required.issubset(df.columns):
            df["InsomniaSeverity_index"] = calculate_insomnia_index(df)
        else:
            missing = sorted(list(required - set(df.columns)))
            st.warning(f"Cannot compute InsomniaSeverity_index (missing columns: {missing}).")

        return df

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


def calculate_insomnia_index(df: pd.DataFrame) -> pd.Series:
    """Calculate a simple insomnia severity score based on key indicators"""
    sleep_difficulty_map = {
        "Never": 0,
        "Rarely (1–2 times a week)": 1,
        "Sometimes (3–4 times a week)": 2,
        "Often (5–6 times a week)": 3,
        "Always (every night)": 4,
    }

    # Sleep quality: 1=worst, 5=best (invert into severity)
    quality_map = {"1": 4, "2": 3, "3": 2, "4": 1, "5": 0}

    score = 0
    score += df["DifficultyFallingAsleep"].map(sleep_difficulty_map).fillna(0)
    score += df["SleepQuality"].astype(str).map(quality_map).fillna(0)
    score += df["NightWakeups"].map(sleep_difficulty_map).fillna(0)

    # Normalize to 0–28 scale
    return (score / 12 * 28).round(1)


def get_data_info(df):
    if df is None or len(df) == 0:
        return None

    return {
        "total_responses": len(df),
        "last_updated": df["Timestamp"].max() if "Timestamp" in df.columns else None,
        "faculties": df["Faculty"].nunique() if "Faculty" in df.columns else None,
        "avg_isi": df["InsomniaSeverity_index"].mean() if "InsomniaSeverity_index" in df.columns else None,
    }


def display_sidebar_info():
    st.sidebar.markdown("### 📊 Data Status")

    if "data" not in st.session_state or st.session_state["data"] is None:
        st.session_state["data"] = load_data()

    df = st.session_state["data"]

    if df is not None:
        info = get_data_info(df)

        st.sidebar.success("✅ Data Loaded Successfully")
        st.sidebar.metric("Total Responses", info["total_responses"])

        if info["last_updated"] is not None:
            st.sidebar.metric("Last Updated", info["last_updated"].strftime("%Y-%m-%d %H:%M"))

        if info["faculties"] is not None:
            st.sidebar.metric("Faculties", info["faculties"])

        if info["avg_isi"] is not None:
            st.sidebar.metric("Avg ISI Score", f"{info['avg_isi']:.1f}")

        st.sidebar.markdown("---")
        st.sidebar.caption("🔄 Auto-refreshes every 5 minutes")

        if st.sidebar.button("🔄 Refresh Now", use_container_width=True):
            st.cache_data.clear()
            st.session_state["data"] = load_data()
            st.rerun()
    else:
        st.sidebar.error("❌ Failed to load data")
        if st.sidebar.button("🔄 Retry", use_container_width=True):
            st.cache_data.clear()
            st.session_state["data"] = load_data()
            st.rerun()


def get_df():
    if "data" not in st.session_state:
        st.session_state["data"] = load_data()
    return st.session_state["data"]
