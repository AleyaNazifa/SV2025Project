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
    # Minimal: if your cleaned file already contains these, nothing breaks.
    df.columns = [clean_colname(c) for c in df.columns]

    # If already exists, skip.
    if "InsomniaSeverity_index" in df.columns:
        return df

    freq5_map = {
        "Never": 0,
        "Rarely (1–2 times a week)": 1,
        "Sometimes (3–4 times a week)": 2,
        "Often (5–6 times a week)": 3,
        "Always (every night)": 4,
        "Always": 4, "Often": 3, "Sometimes": 2, "Rarely": 1
    }

    col_fall = "How often do you have difficulty falling asleep at night?"
    col_wake = "How often do you wake up during the night and have trouble falling back asleep?"

    if "DifficultyFallingAsleep_score" not in df.columns and col_fall in df.columns:
        df["DifficultyFallingAsleep_score"] = df[col_fall].map(freq5_map)

    if "NightWaking_score" not in df.columns and col_wake in df.columns:
        df["NightWaking_score"] = df[col_wake].map(freq5_map)

    if "DifficultyFallingAsleep_score" in df.columns and "NightWaking_score" in df.columns:
        df["InsomniaSeverity_index"] = df[["DifficultyFallingAsleep_score", "NightWaking_score"]].mean(axis=1)

    return df


def load_data_ui():
    st.sidebar.header("Data Source")
    mode = st.sidebar.radio("Select mode", ["Live Google Sheet", "Upload CSV"], index=0)

    if st.sidebar.button("Refresh data"):
        st.cache_data.clear()
        st.rerun()

    if mode == "Live Google Sheet":
        url = st.sidebar.text_input("Published CSV URL", value="")
        if not url.strip():
            st.info("Paste your published Google Sheet CSV URL to continue.")
            return
        df = _read_csv_url(url.strip())
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

