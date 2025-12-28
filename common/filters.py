import streamlit as st

FILTER_COLS = {
    "Gender": "What is your gender?",
    "Age group": "What is your age group?",
    "Year of study": "What is your year of study?",
    "Faculty": "Which faculty are you currently enrolled in?",
}

def apply_sidebar_filters(df):
    st.sidebar.header("Filters")
    df_f = df.copy()

    for label, col in FILTER_COLS.items():
        if col in df_f.columns:
            options = sorted(df_f[col].dropna().unique().tolist())
            selected = st.sidebar.multiselect(label, options, default=options)
            if selected:
                df_f = df_f[df_f[col].isin(selected)]

    # Optional: insomnia severity range filter
    if "InsomniaSeverity_index" in df_f.columns and df_f["InsomniaSeverity_index"].notna().any():
        min_v = float(df_f["InsomniaSeverity_index"].min())
        max_v = float(df_f["InsomniaSeverity_index"].max())
        r = st.sidebar.slider("Insomnia severity range (index)", min_value=min_v, max_value=max_v, value=(min_v, max_v))
        df_f = df_f[(df_f["InsomniaSeverity_index"] >= r[0]) & (df_f["InsomniaSeverity_index"] <= r[1])]

    return df_f

