from __future__ import annotations
import re
import numpy as np
import pandas as pd


# -----------------------------
# Helpers
# -----------------------------
def _norm_col(col: str) -> str:
    s = str(col).replace("\u00A0", " ")
    s = s.replace("\n", " ").replace("\t", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _map_freq(x: object) -> int:
    s = str(x).strip()
    mapping = {
        "Never": 0,
        "Rarely": 1,
        "Occasionally": 2,
        "Sometimes": 2,
        "Often": 3,
        "Frequently": 3,
        "Always": 4,
        "Always (every night)": 4,
    }
    return mapping.get(s, 0)


def _sleep_hours_to_est(val: object) -> float:
    if pd.isna(val):
        return np.nan

    x = str(val).strip()
    mapping = {
        "Less than 4 hours": 3.5,
        "4–5 hours": 4.5,
        "5–6 hours": 5.5,
        "6–7 hours": 6.5,
        "7–8 hours": 7.5,
        "8–9 hours": 8.5,
        "More than 8 hours": 9.0,
        "9 or more hours": 9.0,
    }
    if x in mapping:
        return mapping[x]

    nums = re.findall(r"\d+\.?\d*", x.replace("–", "-"))
    if len(nums) >= 2:
        return (float(nums[0]) + float(nums[1])) / 2
    if len(nums) == 1:
        return float(nums[0])
    return np.nan


def _categorize_insomnia(score: float) -> str | float:
    if pd.isna(score):
        return np.nan
    if score <= 4:
        return "Low / No Insomnia"
    if score <= 8:
        return "Moderate Insomnia"
    return "Severe Insomnia"


# -----------------------------
# Main function
# -----------------------------
def prepare_aelyana_data(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df

    out = df.copy()
    out.columns = [_norm_col(c) for c in out.columns]

    rename_candidates = {
        "How often do you have difficulty falling asleep at night?": "DifficultyFallingAsleep",
        "How often do you wake up during the night and have trouble falling back asleep?": "NightWakeups",
        "How would you rate the overall quality of your sleep?": "SleepQuality",
        "How often do you feel fatigued during the day, affecting your ability to study or attend classes?": "DaytimeFatigue",
        "On average, how many hours of sleep do you get on a typical day?": "SleepHours",
        "How often do you experience difficulty concentrating during lectures or studying due to lack of sleep?": "ConcentrationDifficulty",
        "How often do you miss or skip classes due to sleep-related issues?": "MissedClasses",
        "How would you describe the impact of insufficient sleep on assignments?": "AssignmentImpact",
        "How would you rate your overall academic performance?": "AcademicPerformance",
        "What is your GPA range?": "GPA",
        "What is your CGPA range?": "CGPA",
    }

    out = out.rename(columns={_norm_col(k): v for k, v in rename_candidates.items() if _norm_col(k) in out.columns})

    # ISI-style index
    out["SleepQuality_Score"] = (5 - pd.to_numeric(out.get("SleepQuality"), errors="coerce")).clip(0, 4).fillna(0)
    out["FallingAsleep_Score"] = out.get("DifficultyFallingAsleep", "").map(_map_freq).fillna(0)
    out["NightWakeups_Score"] = out.get("NightWakeups", "").map(_map_freq).fillna(0)
    out["Fatigue_Score"] = out.get("DaytimeFatigue", "").map(_map_freq).fillna(0)

    out["InsomniaSeverity_index"] = (
        out["SleepQuality_Score"]
        + out["FallingAsleep_Score"]
        + out["NightWakeups_Score"]
        + out["Fatigue_Score"]
    )

    out["Insomnia_Category"] = out["InsomniaSeverity_index"].apply(_categorize_insomnia)

    # Numeric features
    out["SleepHours_est"] = out.get("SleepHours", "").apply(_sleep_hours_to_est)

    academic_map = {
        "Below average": 1,
        "Average": 2,
        "Good": 3,
        "Very good": 4,
        "Excellent": 5,
    }
    out["AcademicPerformance_numeric"] = out.get("AcademicPerformance", "").map(academic_map)

    freq_simple = {"Never": 0, "Rarely": 1, "Sometimes": 2, "Often": 3, "Always": 4}
    out["DaytimeFatigue_numeric"] = out.get("DaytimeFatigue", "").map(freq_simple)
    out["ConcentrationDifficulty_numeric"] = out.get("ConcentrationDifficulty", "").map(freq_simple)

    missed_map = {
        "Never": 0,
        "Rarely": 1,
        "Sometimes": 2,
        "Often": 3,
        "Always": 4,
    }
    out["MissedClasses_numeric"] = out.get("MissedClasses", "").map(missed_map)

    gpa_map = {
        "Below 2.00": 1.5,
        "2.00 - 2.99": 2.5,
        "3.00 - 3.69": 3.35,
        "3.70 - 4.00": 3.85,
    }
    out["GPA_numeric"] = out.get("GPA", "").map(gpa_map)
    out["CGPA_numeric"] = out.get("CGPA", "").map(gpa_map)

    return out
