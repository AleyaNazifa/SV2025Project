import re
import pandas as pd
import streamlit as st


def clean_colname(c: str) -> str:
    return re.sub(r"\s+", " ", str(c)).strip()


@st.cache_data(ttl=300, show_spinner=False)
def _read_csv_url(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    df.columns = [clean_colname(c) for c in df.columns]
    return df


@st.cache_data(ttl=300, show_spinner=False)
def _read_csv_upload(uploaded_file) -> pd.DataFrame:
    df = pd.read_csv(uploaded_file)
    df.columns = [clean_colname(c) for c in df.columns]
    return df


def ensure_engineered_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensures engineered columns exist.
    If you upload the cleaned CSV (already includes *_score and indexes), this will not break anything.
    If you upload raw Google Form CSV, this will add the essential columns.
    """
    df.columns = [clean_colname(c) for c in df.columns]

    # Clean object columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    # Mappings
    freq5_map = {
        "Never": 0,
        "Rarely (1–2 times a week)": 1,
        "Sometimes (3–4 times a week)": 2,
        "Often (5–6 times a week)": 3,
        "Always (every night)": 4,
        "Always": 4, "Often": 3, "Sometimes": 2, "Rarely": 1
    }

    sleep_hours_map = {
        "Less than 5 hours": 4.5,
        "5–6 hours": 5.5,
        "7–8 hours": 7.5,
        "More than 8 hours": 8.5
    }

    fatigue_map = {"Never": 0, "Rarely": 1, "Sometimes": 2, "Often": 3, "Always": 4}
    nap_map = {"Never": 0, "Occasionally": 1, "Frequently": 2}

    impact_map = {"No impact": 0, "Minor impact": 1, "Moderate impact": 2, "Major impact": 3, "Severe impact": 4}
    academic_perf_map = {"Below average": 1, "Average": 2, "Good": 3, "Very good": 4, "Excellent": 5}

    stress_map = {"Low stress": 1, "Moderate stress": 2, "High stress": 3, "Extremely high stress": 4}

    # Raw columns
    col_fall = "How often do you have difficulty falling asleep at night?"
    col_hours = "On average, how many hours of sleep do you get on a typical day?"
    col_wake = "How often do you wake up during the night and have trouble falling back asleep?"
    col_quality = "How would you rate the overall quality of your sleep?"
    col_bedtime = "At what time do you usually go to bed on weekdays?"
    col_nap = "Do you usually nap during the day?"

    col_conc = "How often do you experience difficulty concentrating during lectures or studying due to lack of sleep?"
    col_fatigue = "How often do you feel fatigued during the day, affecting your ability to study or attend classes?"
    col_skip = "How often do you miss or skip classes due to sleep-related issues (e.g., insomnia, feeling tired)?"
    col_assign = "How would you describe the impact of insufficient sleep on your ability to complete assignments and meet deadlines?"
    col_perf = "How would you rate your overall academic performance (GPA or grades) in the past semester?"

    col_device = "How often do you use electronic devices (e.g., phone, computer) before going to sleep?"
    col_caffeine = "How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?"
    col_exercise = "How often do you engage in physical activity or exercise?"
    col_stress = "How would you describe your stress levels related to academic workload?"

    # Sleep scores
    if "DifficultyFallingAsleep_score" not in df.columns and col_fall in df.columns:
        df["DifficultyFallingAsleep_score"] = df[col_fall].map(freq5_map)

    if "NightWaking_score" not in df.columns and col_wake in df.columns:
        df["NightWaking_score"] = df[col_wake].map(freq5_map)

    if "SleepHours_est" not in df.columns and col_hours in df.columns:
        df["SleepHours_est"] = df[col_hours].map(sleep_hours_map)

    if "SleepQuality_score" not in df.columns and col_quality in df.columns:
        df["SleepQuality_score"] = pd.to_numeric(df[col_quality], errors="coerce")

    bedtime_map = {"Before 10 PM": 0, "10–11 PM": 1, "11 PM–12 AM": 2, "After 12 AM": 3}
    if "Bedtime_weekday_score" not in df.columns and col_bedtime in df.columns:
        df["Bedtime_weekday_score"] = df[col_bedtime].map(bedtime_map)

    if "Nap_score" not in df.columns and col_nap in df.columns:
        df["Nap_score"] = df[col_nap].map(nap_map)

    # Academic scores
    if "ConcentrationDifficulty_score" not in df.columns and col_conc in df.columns:
        df["ConcentrationDifficulty_score"] = df[col_conc].map(fatigue_map)

    if "DaytimeFatigue_score" not in df.columns and col_fatigue in df.columns:
        df["DaytimeFatigue_score"] = df[col_fatigue].map(fatigue_map)

    skip_classes_map = {
        "Never": 0,
        "Rarely (1–2 times a month)": 1,
        "Sometimes (1–2 times a week)": 2,
        "Often (3–4 times a week)": 3,
        "Always": 4
    }
    if "SkipClasses_score" not in df.columns and col_skip in df.columns:
        df["SkipClasses_score"] = df[col_skip].map(skip_classes_map)

    if "AssignmentImpact_score" not in df.columns and col_assign in df.columns:
        df["AssignmentImpact_score"] = df[col_assign].map(impact_map)

    if "AcademicPerformance_score" not in df.columns and col_perf in df.columns:
        df["AcademicPerformance_score"] = df[col_perf].map(academic_perf_map)

    # Lifestyle
    if "Stress_score" not in df.columns and col_stress in df.columns:
        df["Stress_score"] = df[col_stress].map(stress_map)

    if "DeviceBeforeSleep_score" not in df.columns and col_device in df.columns:
        df["DeviceBeforeSleep_score"] = df[col_device].map(freq5_map)

    caffeine_map = {
        "Never": 0,
        "Rarely (1–2 times a week)": 1,
        "Sometimes (3–4 times a week)": 2,
        "Often (5–6 times a week)": 3,
        "Always (daily)": 4
    }
    if "CaffeineUse_score" not in df.columns and col_caffeine in df.columns:
        df["CaffeineUse_score"] = df[col_caffeine].map(caffeine_map)

    exercise_map = {
        "Never": 0,
        "Rarely (1–2 times a week)": 1,
        "Sometimes (3–4 times a week)": 2,
        "Often (5–6 times a week)": 3,
        "Every day": 4
    }
    if "Exercise_score" not in df.columns and col_exercise in df.columns:
        df["Exercise_score"] = df[col_exercise].map(exercise_map)

    # Indexes
    if "InsomniaSeverity_index" not in df.columns:
        need = ["DifficultyFallingAsleep_score", "NightWaking_score"]
        if all(c in df.columns for c in need):
            df["InsomniaSeverity_index"] = df[need].mean(axis=1)

    if "AcademicImpact_index" not in df.columns:
        need = ["ConcentrationDifficulty_score", "DaytimeFatigue_score", "SkipClasses_score", "AssignmentImpact_score"]
        if all(c in df.columns for c in need):
            df["AcademicImpact_index"] = df[need].mean(axis=1)

    return df


def load_data_ui() -> None:
    """
    Sidebar UI to load either:
    - Live Google Sheet CSV (Option A)
    - Uploaded CSV
    Stores result into st.session_state['df']
    """
    st.sidebar.header("Data Source")
    mode = st.sidebar.radio("Select mode", ["Live Google Sheet (Auto)", "Upload CSV"], index=0)

    refresh_minutes = st.sidebar.slider("Auto refresh (minutes)", 1, 30, 5)
    ttl_seconds = int(refresh_minutes * 60)

    # update cache TTL dynamically by clearing cache when interval changes
    st.session_state["ttl_seconds"] = ttl_seconds

    if st.sidebar.button("Refresh data now"):
        st.cache_data.clear()
        st.rerun()

    if mode == "Live Google Sheet (Auto)":
        csv_url = st.sidebar.text_input("Published Google Sheet CSV URL", value="")
        if not csv_url.strip():
            st.info("Paste your published Google Sheet CSV URL to continue.")
            return

        # set ttl by re-wrapping cache logic: simplest is to just rely on existing 300s cache + manual refresh
        df = _read_csv_url(csv_url.strip())

    else:
        uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"])
        if uploaded is None:
            st.info("Upload a CSV to continue.")
            return
        df = _read_csv_upload(uploaded)

    df = ensure_engineered_columns(df)
    st.session_state["df"] = df


def get_df():
    return st.session_state.get("df", None)
