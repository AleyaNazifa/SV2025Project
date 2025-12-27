import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from data_loader import get_dataframe_from_session

st.title("Insomnia Visualisation")
st.caption("Core scientific visualizations (5 techniques).")

df = get_dataframe_from_session()
if df is None:
    st.warning("No data loaded yet. Go to the main page to load data.")
    st.stop()

st.sidebar.header("Filters")

def multiselect_filter(df, label, col):
    if col not in df.columns:
        return df
    options = sorted(df[col].dropna().unique().tolist())
    selected = st.sidebar.multiselect(label, options, default=options)
    return df[df[col].isin(selected)] if selected else df

df_f = df.copy()
df_f = multiselect_filter(df_f, "Gender", "What is your gender?")
df_f = multiselect_filter(df_f, "Age group", "What is your age group?")
df_f = multiselect_filter(df_f, "Year of study", "What is your year of study?")
df_f = multiselect_filter(df_f, "Faculty", "Which faculty are you currently enrolled in?")

st.write(f"Filtered rows: **{len(df_f)}**")
st.divider()

# Viz 1
st.subheader("1) Distribution of Estimated Sleep Duration")
if "SleepHours_est" in df_f.columns:
    s = df_f["SleepHours_est"].dropna()
    fig = plt.figure(figsize=(7,4))
    plt.hist(s, bins=[4,5,6,7,8,9], edgecolor="black")
    plt.title("Distribution of Estimated Sleep Duration")
    plt.xlabel("Estimated Sleep Hours (category midpoint)")
    plt.ylabel("Number of Respondents")
    plt.xticks([4.5, 5.5, 7.5, 8.5], ["<5", "5–6", "7–8", ">8"])
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)
else:
    st.error("Missing: SleepHours_est")

st.divider()

# Viz 2
st.subheader("2) Insomnia Severity by Sleep Quality (Boxplot)")
need = {"SleepQuality_score", "InsomniaSeverity_index"}
if need.issubset(df_f.columns):
    plot_df = df_f[list(need)].dropna()
    plot_df["SleepQuality_score"] = plot_df["SleepQuality_score"].astype(int)

    levels = sorted(plot_df["SleepQuality_score"].unique())
    data = [plot_df.loc[plot_df["SleepQuality_score"] == lv, "InsomniaSeverity_index"].values for lv in levels]

    fig = plt.figure(figsize=(7,4))
    plt.boxplot(data, labels=levels, showmeans=True)
    plt.title("Insomnia Severity by Self-Rated Sleep Quality")
    plt.xlabel("Sleep Quality Score (1=Poor, 5=Excellent)")
    plt.ylabel("Insomnia Severity Index (0–4)")
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)
else:
    st.error(f"Missing: {sorted(list(need - set(df_f.columns)))}")

st.divider()

# Viz 3
st.subheader("3) Insomnia Severity vs Academic Impact (Scatter + Trendline)")
need = {"InsomniaSeverity_index", "AcademicImpact_index"}
if need.issubset(df_f.columns):
    plot_df = df_f[list(need)].dropna()
    x = plot_df["InsomniaSeverity_index"].to_numpy()
    y = plot_df["AcademicImpact_index"].to_numpy()

    if len(x) >= 2:
        m, b = np.polyfit(x, y, 1)
        r = np.corrcoef(x, y)[0, 1]

        fig = plt.figure(figsize=(7,4))
        plt.scatter(x, y, alpha=0.75, edgecolors="black", linewidths=0.3)
        plt.plot([x.min(), x.max()], [m*x.min()+b, m*x.max()+b])
        plt.title("Insomnia Severity vs Academic Impact")
        plt.xlabel("Insomnia Severity Index (0–4)")
        plt.ylabel("Academic Impact Index (0–4)")
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)

        st.caption(f"Pearson correlation (r): {r:.3f}")
    else:
        st.warning("Not enough filtered data points to compute trendline.")
else:
    st.error(f"Missing: {sorted(list(need - set(df_f.columns)))}")

st.divider()

# Viz 4
st.subheader("4) Academic Performance by Insomnia Severity Group")
need = {"InsomniaSeverity_index", "AcademicPerformance_score"}
if need.issubset(df_f.columns):
    plot_df = df_f[list(need)].dropna()

    def group(v: float) -> str:
        if v < 1.5:
            return "Low"
        if v < 3.0:
            return "Moderate"
        return "High"

    plot_df["InsomniaGroup"] = plot_df["InsomniaSeverity_index"].apply(group)
    order = ["Low", "Moderate", "High"]

    means = plot_df.groupby("InsomniaGroup")["AcademicPerformance_score"].mean().reindex(order)
    counts = plot_df.groupby("InsomniaGroup")["AcademicPerformance_score"].size().reindex(order)

    fig = plt.figure(figsize=(7,4))
    plt.bar(means.index, means.values, edgecolor="black")
    plt.title("Mean Academic Performance by Insomnia Severity Group")
    plt.xlabel("Insomnia Severity Group")
    plt.ylabel("Mean Academic Performance Score (1–5)")
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)

    st.caption("Group counts: " + ", ".join([f"{k}={int(v)}" for k, v in counts.dropna().items()]))
else:
    st.error(f"Missing: {sorted(list(need - set(df_f.columns)))}")

st.divider()

# Viz 5
st.subheader("5) Correlation Heatmap")
corr_cols = [
    "SleepHours_est", "SleepQuality_score", "InsomniaSeverity_index",
    "AcademicImpact_index", "Stress_score", "AcademicPerformance_score",
    "DeviceBeforeSleep_score", "CaffeineUse_score", "Exercise_score"
]
missing = [c for c in corr_cols if c not in df_f.columns]
if missing:
    st.error(f"Missing for heatmap: {missing}")
else:
    corr_df = df_f[corr_cols].dropna()
    if len(corr_df) < 3:
        st.warning("Not enough filtered data rows for stable correlation matrix.")
    else:
        corr = corr_df.corr(numeric_only=True)

        fig = plt.figure(figsize=(9,6))
        im = plt.imshow(corr.values)
        plt.title("Correlation Heatmap: Sleep, Stress, Academic Variables")
        plt.xticks(range(len(corr_cols)), corr_cols, rotation=60, ha="right")
        plt.yticks(range(len(corr_cols)), corr_cols)

        for i in range(len(corr_cols)):
            for j in range(len(corr_cols)):
                plt.text(j, i, f"{corr.values[i, j]:.2f}", ha="center", va="center", fontsize=8)

        plt.colorbar(im, fraction=0.046, pad=0.04)
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
