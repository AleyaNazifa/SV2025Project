import matplotlib.pyplot as plt
import streamlit as st

def apply_filters(df):
    st.sidebar.subheader("Filters")
    df_f = df.copy()

    for col in [
        "What is your gender?",
        "What is your age group?",
        "What is your year of study?",
        "Which faculty are you currently enrolled in?"
    ]:
        if col in df_f.columns:
            options = sorted(df_f[col].dropna().unique().tolist())
            selected = st.sidebar.multiselect(col, options, default=options)
            if selected:
                df_f = df_f[df_f[col].isin(selected)]
    return df_f


def render(df):
    st.header("🛌 Sleep & Insomnia Overview — AleyaAelyana")
    st.write("Objective: Describe baseline sleep patterns and insomnia symptom profiles.")

    df_f = apply_filters(df)

    st.subheader("📊 Summary Box")
    c1, c2, c3 = st.columns(3)
    c1.metric("Filtered Responses", f"{len(df_f)}")
    c2.metric("Mean Sleep Hours", f"{df_f['SleepHours_est'].dropna().mean():.2f}" if "SleepHours_est" in df_f else "N/A")
    c3.metric("Mean Insomnia Index", f"{df_f['InsomniaSeverity_index'].dropna().mean():.2f}" if "InsomniaSeverity_index" in df_f else "N/A")

    st.markdown("---")

    # 1) Sleep duration histogram
    st.subheader("1) Sleep Duration Distribution")
    if "SleepHours_est" in df_f.columns:
        s = df_f["SleepHours_est"].dropna()
        fig = plt.figure(figsize=(7,4))
        plt.hist(s, bins=[4,5,6,7,8,9], edgecolor="black")
        plt.xlabel("Estimated Sleep Hours")
        plt.ylabel("Count")
        plt.title("Sleep Duration Distribution")
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
    else:
        st.error("Missing: SleepHours_est")

    # 2) Bedtime distribution
    st.subheader("2) Bedtime (Weekdays) Distribution")
    col = "At what time do you usually go to bed on weekdays?"
    if col in df_f.columns:
        counts = df_f[col].value_counts()
        fig = plt.figure(figsize=(7,4))
        plt.bar(counts.index.astype(str), counts.values, edgecolor="black")
        plt.xticks(rotation=20, ha="right")
        plt.xlabel("Bedtime")
        plt.ylabel("Count")
        plt.title("Weekday Bedtime Distribution")
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
    else:
        st.error(f"Missing: {col}")

    # 3) Sleep quality distribution
    st.subheader("3) Sleep Quality Distribution")
    if "SleepQuality_score" in df_f.columns:
        counts = df_f["SleepQuality_score"].dropna().astype(int).value_counts().sort_index()
        fig = plt.figure(figsize=(7,4))
        plt.bar(counts.index.astype(str), counts.values, edgecolor="black")
        plt.xlabel("Sleep Quality (1–5)")
        plt.ylabel("Count")
        plt.title("Sleep Quality Distribution")
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
    else:
        st.error("Missing: SleepQuality_score")

    # 4) Mean symptom scores
    st.subheader("4) Mean Insomnia Symptom Scores")
    needed = ["DifficultyFallingAsleep_score", "NightWaking_score"]
    if all(c in df_f.columns for c in needed):
        means = df_f[needed].mean()
        fig = plt.figure(figsize=(7,4))
        plt.bar(means.index, means.values, edgecolor="black")
        plt.ylabel("Mean Score (0–4)")
        plt.title("Mean Insomnia Symptoms")
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
    else:
        st.error("Missing symptom score columns.")

    # 5) Insomnia by nap behavior (boxplot)
    st.subheader("5) Insomnia Severity by Nap Frequency")
    if "Nap_score" in df_f.columns and "InsomniaSeverity_index" in df_f.columns:
        plot_df = df_f[["Nap_score", "InsomniaSeverity_index"]].dropna()
        levels = sorted(plot_df["Nap_score"].unique())
        data = [plot_df.loc[plot_df["Nap_score"] == lv, "InsomniaSeverity_index"].values for lv in levels]
        fig = plt.figure(figsize=(7,4))
        plt.boxplot(data, labels=levels, showmeans=True)
        plt.xlabel("Nap Score (0=Never,1=Occasionally,2=Frequently)")
        plt.ylabel("Insomnia Index")
        plt.title("Insomnia Severity by Nap Frequency")
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
    else:
        st.error("Missing: Nap_score / InsomniaSeverity_index")
