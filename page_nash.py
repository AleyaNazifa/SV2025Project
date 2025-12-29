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
    st.header("⚙️ Lifestyle, Stress & Factors — Nash")
    st.write("Objective: Explore lifestyle and stress factors associated with insomnia and academic impact.")

    df_f = apply_filters(df)

    st.subheader("📊 Summary Box")
    c1, c2, c3 = st.columns(3)
    c1.metric("Filtered Responses", f"{len(df_f)}")
    c2.metric("Mean Stress", f"{df_f['Stress_score'].dropna().mean():.2f}" if "Stress_score" in df_f else "N/A")
    c3.metric("Mean Device Use", f"{df_f['DeviceBeforeSleep_score'].dropna().mean():.2f}" if "DeviceBeforeSleep_score" in df_f else "N/A")

    st.markdown("---")

    # 1) Sleep quality by device use (boxplot)
    st.subheader("1) Sleep Quality by Device Use Before Sleep")
    if {"DeviceBeforeSleep_score", "SleepQuality_score"}.issubset(df_f.columns):
        plot_df = df_f[["DeviceBeforeSleep_score", "SleepQuality_score"]].dropna()
        levels = sorted(plot_df["DeviceBeforeSleep_score"].unique())
        data = [plot_df.loc[plot_df["DeviceBeforeSleep_score"] == lv, "SleepQuality_score"].values for lv in levels]
        fig = plt.figure(figsize=(7,4))
        plt.boxplot(data, labels=levels, showmeans=True)
        plt.xlabel("Device Use Score (0–4)")
        plt.ylabel("Sleep Quality (1–5)")
        plt.title("Sleep Quality by Device Use")
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
    else:
        st.error("Missing: DeviceBeforeSleep_score / SleepQuality_score")

    # 2) Insomnia severity by caffeine (boxplot)
    st.subheader("2) Insomnia Severity by Caffeine Use")
    if {"CaffeineUse_score", "InsomniaSeverity_index"}.issubset(df_f.columns):
        plot_df = df_f[["CaffeineUse_score", "InsomniaSeverity_index"]].dropna()
        levels = sorted(plot_df["CaffeineUse_score"].unique())
        data = [plot_df.loc[plot_df["CaffeineUse_score"] == lv, "InsomniaSeverity_index"].values for lv in levels]
        fig = plt.figure(figsize=(7,4))
        plt.boxplot(data, labels=levels, showmeans=True)
        plt.xlabel("Caffeine Use Score (0–4)")
        plt.ylabel("Insomnia Severity Index (0–4)")
        plt.title("Insomnia Severity by Caffeine Use")
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
    else:
        st.error("Missing: CaffeineUse_score / InsomniaSeverity_index")

    # 3) Insomnia severity by exercise (boxplot)
    st.subheader("3) Insomnia Severity by Exercise Frequency")
    if {"Exercise_score", "InsomniaSeverity_index"}.issubset(df_f.columns):
        plot_df = df_f[["Exercise_score", "InsomniaSeverity_index"]].dropna()
        levels = sorted(plot_df["Exercise_score"].unique())
        data = [plot_df.loc[plot_df["Exercise_score"] == lv, "InsomniaSeverity_index"].values for lv in levels]
        fig = plt.figure(figsize=(7,4))
        plt.boxplot(data, labels=levels, showmeans=True)
        plt.xlabel("Exercise Score (0–4)")
        plt.ylabel("Insomnia Severity Index (0–4)")
        plt.title("Insomnia Severity by Exercise")
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
    else:
        st.error("Missing: Exercise_score / InsomniaSeverity_index")

    # 4) Academic impact by stress (boxplot)
    st.subheader("4) Academic Impact by Stress Level")
    if {"Stress_score", "AcademicImpact_index"}.issubset(df_f.columns):
        plot_df = df_f[["Stress_score", "AcademicImpact_index"]].dropna()
        levels = sorted(plot_df["Stress_score"].unique())
        data = [plot_df.loc[plot_df["Stress_score"] == lv, "AcademicImpact_index"].values for lv in levels]
        fig = plt.figure(figsize=(7,4))
        plt.boxplot(data, labels=levels, showmeans=True)
        plt.xlabel("Stress Score (1–4)")
        plt.ylabel("Academic Impact Index (0–4)")
        plt.title("Academic Impact by Stress")
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
    else:
        st.error("Missing: Stress_score / AcademicImpact_index")

    # 5) Lifestyle correlation heatmap
    st.subheader("5) Correlation Heatmap (Lifestyle Focus)")
    corr_cols = [
        "DeviceBeforeSleep_score",
        "CaffeineUse_score",
        "Exercise_score",
        "Stress_score",
        "InsomniaSeverity_index",
        "SleepQuality_score",
        "AcademicImpact_index",
    ]
    missing = [c for c in corr_cols if c not in df_f.columns]
    if missing:
        st.error(f"Missing: {missing}")
    else:
        corr_df = df_f[corr_cols].dropna()
        if len(corr_df) < 3:
            st.warning("Not enough rows after filtering for stable correlations.")
        else:
            corr = corr_df.corr(numeric_only=True)
            fig = plt.figure(figsize=(9,5))
            im = plt.imshow(corr.values)
            plt.title("Correlation Heatmap (Lifestyle)")
            plt.xticks(range(len(corr_cols)), corr_cols, rotation=60, ha="right")
            plt.yticks(range(len(corr_cols)), corr_cols)
            for i in range(len(corr_cols)):
                for j in range(len(corr_cols)):
                    plt.text(j, i, f"{corr.values[i,j]:.2f}", ha="center", va="center", fontsize=8)
            plt.colorbar(im, fraction=0.046, pad=0.04)
            plt.tight_layout()
            st.pyplot(fig, clear_figure=True)
