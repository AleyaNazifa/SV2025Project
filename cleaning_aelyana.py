# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

st.set_page_config(page_title="Insomnia & Education Survey Analysis", layout="wide")
st.title("Insomnia and Educational Survey Outcomes among UMK Students")

# =========================================================
# 1. FILE UPLOAD
# =========================================================
st.header("Upload Your CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("Data loaded successfully!")
        st.subheader("Raw Data Preview")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Error loading data: {e}")
else:
    st.info("Please upload a CSV file to continue.")

# =========================================================
# 2. INITIAL DATA CHECKING
# =========================================================
if uploaded_file:
    st.header("Data Quality Check")
    
    st.subheader("Missing Values per Column")
    missing_values = df.isnull().sum()
    st.dataframe(missing_values)
    
    st.subheader("Duplicate Rows")
    duplicate_rows = df[df.duplicated()]
    st.write(f"Number of duplicate rows: {len(duplicate_rows)}")
    if not duplicate_rows.empty:
        st.dataframe(duplicate_rows.head())
    else:
        st.write("No duplicate rows found.")

# =========================================================
# 3. RENAME COLUMNS
# =========================================================
if uploaded_file:
    new_column_names = [
        'Timestamp','Gender','AgeGroup','YearOfStudy','Faculty',
        'DifficultyFallingAsleep','SleepHours','NightWakeups','SleepQuality',
        'BedTime','DayNap','ConcentrationDifficulty','DaytimeFatigue',
        'MissedClasses','AssignmentImpact','ExamSleepChange',
        'AcademicPerformance','GPA','CGPA','DeviceUsage',
        'CaffeineConsumption','PhysicalActivity','StressLevel','SleepMethods'
    ]
    
    df.columns = new_column_names
    st.subheader("Data with Renamed Columns")
    st.dataframe(df.head())

# =========================================================
# 4. INSOMNIA SEVERITY INDEX (ISI)
# =========================================================
if uploaded_file:
    freq_mapping = {
        'Never': 0,
        'Rarely (1–2 times a month)': 1,
        'Rarely (1–2 times a week)': 1,
        'Rarely': 1,
        'Sometimes (3–4 times a week)': 2,
        'Occasionally': 2,
        'Sometimes': 2,
        'Often (5–6 times a week)': 3,
        'Frequently': 3,
        'Often': 3,
        'Always (every night)': 4,
        'Always': 4
    }

    df['SleepQuality_Score'] = 5 - df['SleepQuality']
    df['FallingAsleep_Score'] = df['DifficultyFallingAsleep'].map(freq_mapping).fillna(0)
    df['NightWakeups_Score'] = df['NightWakeups'].map(freq_mapping).fillna(0)
    df['Fatigue_Score'] = df['DaytimeFatigue'].map(freq_mapping).fillna(0)

    df['InsomniaSeverity_index'] = (
        df['FallingAsleep_Score'] +
        df['NightWakeups_Score'] +
        df['SleepQuality_Score'] +
        df['Fatigue_Score']
    )

    def categorize_insomnia(score):
        if score <= 4:
            return 'Low / No Insomnia'
        elif score <= 8:
            return 'Moderate Insomnia'
        else:
            return 'Severe Insomnia'

    df['Insomnia_Category'] = df['InsomniaSeverity_index'].apply(categorize_insomnia)

    st.subheader("Insomnia Severity Index and Category")
    st.dataframe(df[['InsomniaSeverity_index','Insomnia_Category']].head())

# =========================================================
# 5. FEATURE ENGINEERING
# =========================================================
if uploaded_file:
    st.header("Feature Engineering")

    # Sleep Hours
    sleep_hours_mapping = {
        'Less than 5 hours': 2.5,
        '5–6 hours': 5.5,
        '7–8 hours': 7.5,
        'More than 8 hours': 9.0
    }
    df['SleepHours_est'] = df['SleepHours'].map(sleep_hours_mapping)

    # Academic Performance
    academic_performance_mapping = {
        'Poor':0,'Fair':1,'Average':2,'Good':3,'Very good':4,'Excellent':5
    }
    df['AcademicPerformance_numeric'] = df['AcademicPerformance'].map(academic_performance_mapping)

    # Daytime Fatigue
    daytime_fatigue_mapping = {'Never':0,'Rarely':1,'Sometimes':2,'Often':3,'Always':4}
    df['DaytimeFatigue_numeric'] = df['DaytimeFatigue'].map(daytime_fatigue_mapping).fillna(0)

    # Missed Classes
    missed_classes_mapping = {
        'Never':0,'Rarely (1–2 times a month)':1,
        'Sometimes (3–4 times a month)':2,
        'Often (5–6 times a month)':3,
        'Always (every day)':4
    }
    df['MissedClasses_numeric'] = df['MissedClasses'].map(missed_classes_mapping).fillna(0)

    # GPA & CGPA
    gpa_mapping = {
        'Below 2.00':1.5,
        '2.00 - 2.99':2.5,
        '3.00 - 3.69':3.35,
        '3.70 - 4.00':3.85
    }
    df['GPA_numeric'] = df['GPA'].map(gpa_mapping).fillna(0)
    df['CGPA_numeric'] = df['CGPA'].map(gpa_mapping).fillna(0)

    # Concentration Difficulty
    concentration_mapping = {'Never':0,'Rarely':1,'Sometimes':2,'Often':3,'Always':4}
    df['ConcentrationDifficulty_numeric'] = df['ConcentrationDifficulty'].map(concentration_mapping).fillna(0)

    st.success("Feature engineering completed!")

# =========================================================
# 6. SAVE FINAL DATASET
# =========================================================
if uploaded_file:
    st.header("Download Processed Dataset")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='final_processed_data.csv',
        mime='text/csv',
    )

