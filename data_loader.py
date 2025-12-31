import streamlit as st
import pandas as pd
import numpy as np
import re

# Your published Google Sheet CSV (keep yours)
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSf4umx6QNDel99If8P2otizAHj7jEDxFIsqandbD0zYVzfDheZo2YVkK1_zknpDKjHnBuYWCINgcCe/pub?output=csv"


def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Fix whitespace issues in headers (your sheet has trailing spaces)
    df.columns = [str(c).strip() for c in df.columns]
    return df


def _sleep_hours_to_estimate(x: str) -> float:
    """
    Convert categories like:
    - '7–8 hours' -> 7.5
    - '5–6 hours' -> 5.5
    - 'More than 8 hours' -> 8.5
    - 'Less than 4 hours' -> 3.5
    """
    s = str(x).strip().lower().replace("–", "-")

    if "more than" in s:
        nums = re.findall(r"\d+", s)
        return float(nums[0]) + 0.5 if nums else np.nan

    if "less than" in s:
        nums = re.findall(r"\d+", s)
        return float(nums[0]) - 0.5 if nums else np.nan

    nums = re.findall(r"\d+", s)
    if len(nums) >= 2:
        return (float(nums[0]) + float(nums[1])) / 2
    if len(nums) == 1:
        return float(nums[0])

    return np.nan


def _map_frequency_to_score(x: str) -> int:
    mapping = {
        "Never": 0,
        "Rarely (1–2 times a week)": 1,
        "Rarely (1-2 times a week)": 1,
        "Sometimes (3–4 times a week)": 2,
        "Sometimes (3-4 times a week)": 2,
        "Often (5–6 times a week)": 3,
        "Often (5-6 times a week)": 3,
        "Always (every night)": 4,
    }
    return mapping.get(str(x).strip(), 0)


def _calculate_isi(df: pd.DataFrame) -> pd.Series:
    # A simple ISI-like index (0–28) based on key indicators
    diff = df["DifficultyFallingAsleep"].astype(str).map(_map_frequency_to_score).fillna(0)
    wake = df["NightWakeups"].astype(str).map(_map_frequency_to_score).fillna(0)

    # SleepQuality is 1..5 where 1=poor, 5=excellent → invert to risk
    # quality_risk: 5->0, 4->1, 3->2, 2->3, 1->4
    q = pd.to_numeric(df["SleepQuality"], errors="coerce")
    quality_risk = (5 - q).clip(lower=0, upper=4).fillna(0)

    raw = diff + wake + quality_risk  # 0..12
    isi = (raw / 12 * 28).round(1)    # scale to 0..28
    return isi


def _calculate_lifestyle_risk(df: pd.DataFrame) -> pd.Series:
    def row_risk(row) -> int:
        risk = 0

        device = str(row.get("DeviceUsage", ""))
        if "Always" in device:
            risk += 3
        elif "Often" in device:
            risk += 2

        caff = str(row.get("CaffeineConsumption", ""))
        if "Always" in caff:
            risk += 3
        elif "Often" in caff:
            risk += 2

        activity = str(row.get("PhysicalActivity", ""))
        if ("Never" in activity) or ("Rarely" in activity):
            risk += 2

        stress = str(row.get("StressLevel", ""))
        if "Extremely" in stress:
            risk += 3
        elif "High" in stress:
            risk += 2

        return risk

    return df.apply(row_risk, axis=1)


@st.cache_data(ttl=300)
def load_data() -> pd.DataFrame:
    df = pd.read_csv(GOOGLE_SHEETS_URL)
    df = _clean_columns(df)

    # Robust rename (after stripping)
    col_map = {
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

    # Apply rename for columns that exist (safe)
    df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})

    # Parse timestamp safely
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

    # Derived numeric columns used by Plotly pages
    if "SleepHours" in df.columns:
        df["SleepHours_est"] = df["SleepHours"].map(_sleep_hours_to_estimate)

    # Compute indices if core columns exist
    required_for_isi = {"DifficultyFallingAsleep", "NightWakeups", "SleepQuality"}
    if required_for_isi.issubset(df.columns):
        df["InsomniaSeverity_index"] = _calculate_isi(df)
    else:
        df["InsomniaSeverity_index"] = np.nan

    required_for_risk = {"DeviceUsage", "CaffeineConsumption", "PhysicalActivity", "StressLevel"}
    if required_for_risk.issubset(df.columns):
        df["Lifestyle_Risk"] = _calculate_lifestyle_risk(df)
    else:
        df["Lifestyle_Risk"] = 0

    return df


def get_data_info(df: pd.DataFrame) -> dict:
    return {
        "total_responses": int(len(df)),
        "last_updated": df["Timestamp"].max() if "Timestamp" in df.columns else None,
        "faculties": int(df["Faculty"].nunique()) if "Faculty" in df.columns else 0,
        "avg_isi": float(pd.to_numeric(df["InsomniaSeverity_index"], errors="coerce").mean())
        if "InsomniaSeverity_index" in df.columns
        else float("nan"),
    }


def display_sidebar_info():
    st.sidebar.markdown("### 📊 Data Status")

    if "data" not in st.session_state or st.session_state.data is None:
        st.session_state.data = load_data()

    df = st.session_state.data
    if df is None or len(df) == 0:
        st.sidebar.error("❌ Failed to load data.")
        if st.sidebar.button("🔄 Retry", use_container_width=True):
            st.cache_data.clear()
            st.session_state.data = load_data()
            st.rerun()
        return

    info = get_data_info(df)
    st.sidebar.success("✅ Data Loaded")

    st.sidebar.metric("Total Responses", info["total_responses"])
    if info["last_updated"] is not None and pd.notna(info["last_updated"]):
        st.sidebar.metric("Last Updated", info["last_updated"].strftime("%Y-%m-%d %H:%M"))
    st.sidebar.metric("Faculties", info["faculties"])
    if not np.isnan(info["avg_isi"]):
        st.sidebar.metric("Avg ISI", f"{info['avg_isi']:.1f}")

    st.sidebar.caption("🔄 Auto-refresh every 5 minutes")
    if st.sidebar.button("🔄 Refresh Now", use_container_width=True):
        st.cache_data.clear()
        st.session_state.data = load_data()
        st.rerun()


def get_df():
    if "data" not in st.session_state or st.session_state.data is None:
        st.session_state.data = load_data()
    return st.session_state.data
