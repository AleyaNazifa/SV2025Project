import numpy as np
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

def insomnia_group(v: float) -> str:
    if v < 1.5:
        return "Low"
    if v < 3.0:
        return "Moderate"
    return "High"


def render(df):
    st.header("📚 Academic Impact & Performance — AleyaNazifa")
    st.write("Objective: Evaluate relationships between insomnia severity and academic outcomes.")

    df_f = apply_filters(df)

    st.subheader("📊 Summary Box")
    c1, c2, c3 = st.columns(3)
    c1.metric("Filtered Responses", f"{len(df_f)}")
    c2.metric("Mean Academic Impact", f"{df_f['AcademicImpact_index'].dropna().mean():.2f}" if "AcademicImpact_index" in df_f else "N/A")
    c3.metric("Mean Academic Performance", f"{df_f['AcademicPerformance_score'].dropna().mean():.2f}" if "AcademicPerformance_score" in df_f else "N/A")

    st.markdown("---")

    # 1) Scatter insomnia vs academic impact
    st.subheader("1) Insomnia Severity vs Academic Impact")
    if {"InsomniaSeverity_index", "AcademicImpact_index"}.issubset(df_f.columns):
        plot_df = df_f[["InsomniaSeverity_index", "AcademicImpact_index"]].dropna()
        x = plot_df["InsomniaSeverity_index"].to_numpy()
        y = plot_df["AcademicImpact_index"].to_numpy()

        if len(x) >= 2:
            m, b = np.polyfit(x, y, 1)
            r = np.corrcoef(x, y)[0, 1]
            fig = plt.figure(figsize=(7,4))
            plt.scatter(x, y, alpha=0.75, edgecolors="black", linewidths=0.3)
            plt.plot([x.min(), x.max()], [m*x.min()+b, m*x.max()+b])
            plt.xlabel("Insomnia Severity Index")
            plt.ylabel("Academic Impact Index")
            plt.title("Insomnia vs Academic Impact")
            plt.tight_layout()
            st.pyplot(fig, clear_figure=True)
            st.caption(f"Pearson r = {r:.3f}")
        else:
            st.warning("Not enough data to compute trendline.")
    else:
        st.error("Missing: InsomniaSeverity_index / AcademicImpact_index")

    # 2) Academic impact by sleep quality (boxplot)
    st.subheader("2) Academic Impact by Sleep Quality")
    if {"SleepQuality_score", "AcademicImpact_index"}.issubset(df_f.columns):
        plot_df = df_f[["SleepQuality_score", "AcademicImpact_index"]].dropna()
        plot_df["SleepQuality_score"] = plot_df["SleepQuality_score"].astype(int)
        levels = sorted(plot_df["SleepQuality_score"].unique())
        data = [plot_df.loc[plot_df["SleepQuality_score"] == lv, "AcademicImpact_index"].values for lv in levels]

        fig = plt.figure(figsize=(7,4))
        plt.boxplot(data, labels=levels, showmeans=True)
        plt.xlabel("Sleep Quality (1–5)")
        plt.ylabel("Academic Impact Index")
        plt.title("Academic Impact by Sleep Quality")
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
    else:
        st.error("Missing: SleepQuality_score / AcademicImpact_index")

    # 3) Mean academic performance by insomnia group (bar)
    st.subheader("3) Academic Performance by Insomnia Group")
    if {"InsomniaSeverity_index", "AcademicPerformance_score"}.issubset(df_f.columns):
        plot_df = df_f[["InsomniaSeverity_index", "AcademicPerformance_score"]].dropna()
        plot_df["Group"] = plot_df["InsomniaSeverity_index"].apply(insomnia_group)
        means = plot_df.groupby("Group")["AcademicPerformance_score"].mean().reindex(["Low","Moderate","High"])

        fig = plt.figure(figsize=(7,4))
        plt.bar(means.index, means.values, edgecolor="black")
        plt.xlabel("Insomnia Group")
        plt.ylabel("Mean Academic Performance (1–5)")
        plt.title("Academic Performance by Insomnia Group")
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
    else:
        st.error("Missing: InsomniaSeverity_index / AcademicPerformance_score")

    # 4) Academic correlation heatmap
    st.subheader("4) Correlation Heatmap (Academic Variables)")
    corr_cols = [
        "ConcentrationDifficulty_score",
        "DaytimeFatigue_score",
        "SkipClasses_score",
        "AssignmentImpact_score",
        "AcademicPerformance_score",
        "InsomniaSeverity_index",
        "AcademicImpact_index",
    ]
    if all(c in df_f.columns for c in corr_cols):
        corr_df = df_f[corr_cols].dropna()
        if len(corr_df) >= 3:
            corr = corr_df.corr(numeric_only=True)
            fig = plt.figure(figsize=(9,5))
            im = plt.imshow(corr.values)
            plt.title("Correlation Heatmap (Academic)")
            plt.xticks(range(len(corr_cols)), corr_cols, rotation=60, ha="right")
            plt.yticks(range(len(corr_cols)), corr_cols)
            for i in range(len(corr_cols)):
                for j in range(len(corr_cols)):
                    plt.text(j, i, f"{corr.values[i,j]:.2f}", ha="center", va="center", fontsize=8)
            plt.colorbar(im, fraction=0.046, pad=0.04)
            plt.tight_layout()
            st.pyplot(fig, clear_figure=True)
        else:
            st.warning("Not enough rows after filtering for stable correlations.")
    else:
        st.error("Missing some academic columns for correlation heatmap.")

    # 5) Mean skipping classes by insomnia group
    st.subheader("5) Class Skipping by Insomnia Group")
    if {"InsomniaSeverity_index", "SkipClasses_score"}.issubset(df_f.columns):
        plot_df = df_f[["InsomniaSeverity_index", "SkipClasses_score"]].dropna()
        plot_df["Group"] = plot_df["InsomniaSeverity_index"].apply(insomnia_group)
        means = plot_df.groupby("Group")["SkipClasses_score"].mean().reindex(["Low","Moderate","High"])

        fig = plt.figure(figsize=(7,4))
        plt.bar(means.index, means.values, edgecolor="black")
        plt.xlabel("Insomnia Group")
        plt.ylabel("Mean Skip Classes Score")
        plt.title("Class Skipping by Insomnia Group")
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
    else:
        st.error("Missing: InsomniaSeverity_index / SkipClasses_score")
