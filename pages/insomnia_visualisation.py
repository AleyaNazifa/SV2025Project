import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from data_loader import get_dataframe_from_session

st.title("📈 Insomnia Visualisation")
st.markdown("### Five comprehensive scientific visualizations")
st.divider()

df = get_dataframe_from_session()
if df is None:
    st.warning("⚠️ No data loaded. Go to main page to load data.")
    st.stop()

# Filters
st.sidebar.markdown("### 🎯 Filters")

def multiselect_filter(df, label, col):
    if col not in df.columns:
        return df
    options = sorted(df[col].dropna().unique().tolist())
    selected = st.sidebar.multiselect(f"{label}", options, default=options)
    return df[df[col].isin(selected)] if selected else df

df_f = df.copy()
df_f = multiselect_filter(df_f, "Gender", "What is your gender?")
df_f = multiselect_filter(df_f, "Age", "What is your age group?")
df_f = multiselect_filter(df_f, "Year", "What is your year of study?")
df_f = multiselect_filter(df_f, "Faculty", "Which faculty are you currently enrolled in?")

st.info(f"📊 Showing {len(df_f)} of {len(df)} responses ({len(df_f)/len(df)*100:.1f}%)")

plt.style.use('seaborn-v0_8-whitegrid')

# Viz 1
st.markdown("### 1️⃣ Sleep Duration Distribution")
if "SleepHours_est" in df_f.columns:
    s = df_f["SleepHours_est"].dropna()
    fig, ax = plt.subplots(figsize=(10, 5))
    
    n, bins, patches = ax.hist(s, bins=[4,5,6,7,8,9], edgecolor="white", linewidth=2)
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(patches)))
    for patch, color in zip(patches, colors):
        patch.set_facecolor(color)
    
    ax.set_title("Sleep Duration Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Hours", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    ax.set_xticks([4.5, 5.5, 7.5, 8.5])
    ax.set_xticklabels(["<5h", "5-6h", "7-8h", ">8h"])
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)
else:
    st.error("Missing data")

st.divider()

# Viz 2
st.markdown("### 2️⃣ Insomnia by Sleep Quality")
need = {"SleepQuality_score", "InsomniaSeverity_index"}
if need.issubset(df_f.columns):
    plot_df = df_f[list(need)].dropna()
    plot_df["SleepQuality_score"] = plot_df["SleepQuality_score"].astype(int)

    levels = sorted(plot_df["SleepQuality_score"].unique())
    data = [plot_df.loc[plot_df["SleepQuality_score"] == lv, "InsomniaSeverity_index"].values for lv in levels]

    fig, ax = plt.subplots(figsize=(10, 5))
    bp = ax.boxplot(data, labels=levels, showmeans=True, patch_artist=True,
                    boxprops=dict(facecolor='#3b82f6', alpha=0.7),
                    medianprops=dict(color='red', linewidth=2),
                    meanprops=dict(marker='D', markerfacecolor='orange', markersize=8))
    
    ax.set_title("Insomnia Severity by Sleep Quality", fontsize=14, fontweight='bold')
    ax.set_xlabel("Sleep Quality (1=Poor, 5=Excellent)", fontsize=12)
    ax.set_ylabel("Insomnia Index", fontsize=12)
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)
else:
    st.error("Missing columns")

st.divider()

# Viz 3
st.markdown("### 3️⃣ Insomnia vs Academic Impact")
need = {"InsomniaSeverity_index", "AcademicImpact_index"}
if need.issubset(df_f.columns):
    plot_df = df_f[list(need)].dropna()
    x = plot_df["InsomniaSeverity_index"].to_numpy()
    y = plot_df["AcademicImpact_index"].to_numpy()

    if len(x) >= 2:
        m, b = np.polyfit(x, y, 1)
        r = np.corrcoef(x, y)[0, 1]

        fig, ax = plt.subplots(figsize=(10, 5))
        scatter = ax.scatter(x, y, alpha=0.6, s=80, c=y, cmap='RdYlBu_r', edgecolors="black", linewidths=0.5)
        ax.plot([x.min(), x.max()], [m*x.min()+b, m*x.max()+b], 'r--', linewidth=2, label=f'r={r:.3f}')
        
        ax.set_title("Insomnia vs Academic Impact", fontsize=14, fontweight='bold')
        ax.set_xlabel("Insomnia Index", fontsize=12)
        ax.set_ylabel("Academic Impact", fontsize=12)
        ax.legend()
        plt.colorbar(scatter, ax=ax, label='Impact')
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
        st.caption(f"Correlation: **{r:.3f}**")
else:
    st.error("Missing columns")

st.divider()

# Viz 4
st.markdown("### 4️⃣ Performance by Insomnia Group")
need = {"InsomniaSeverity_index", "AcademicPerformance_score"}
if need.issubset(df_f.columns):
    plot_df = df_f[list(need)].dropna()

    def group(v):
        if v < 1.5: return "Low"
        if v < 3.0: return "Moderate"
        return "High"

    plot_df["Group"] = plot_df["InsomniaSeverity_index"].apply(group)
    order = ["Low", "Moderate", "High"]
    means = plot_df.groupby("Group")["AcademicPerformance_score"].mean().reindex(order)
    counts = plot_df.groupby("Group")["AcademicPerformance_score"].size().reindex(order)

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['#10b981', '#f59e0b', '#ef4444']
    bars = ax.bar(means.index, means.values, color=colors, edgecolor="black", linewidth=2, alpha=0.8)
    
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}\n(n={int(count)})',
                ha='center', va='bottom', fontweight='bold')
    
    ax.set_title("Academic Performance by Insomnia Group", fontsize=14, fontweight='bold')
    ax.set_xlabel("Group", fontsize=12)
    ax.set_ylabel("Performance Score", fontsize=12)
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)
else:
    st.error("Missing columns")

st.divider()

# Viz 5
st.markdown("### 5️⃣ Correlation Heatmap")
corr_cols = [
    "SleepHours_est", "SleepQuality_score", "InsomniaSeverity_index",
    "AcademicImpact_index", "Stress_score", "AcademicPerformance_score",
    "DeviceBeforeSleep_score", "CaffeineUse_score", "Exercise_score"
]

missing = [c for c in corr_cols if c not in df_f.columns]
if not missing:
    corr_df = df_f[corr_cols].dropna()
    if len(corr_df) >= 3:
        corr = corr_df.corr()

        fig, ax = plt.subplots(figsize=(12, 8))
        im = ax.imshow(corr.values, cmap='RdBu_r', vmin=-1, vmax=1)
        
        ax.set_title("Correlation Matrix", fontsize=14, fontweight='bold')
        labels = ["Sleep Hrs", "Quality", "Insomnia", "Impact", "Stress", "Perf", "Device", "Caffeine", "Exercise"]
        ax.set_xticks(range(len(labels)))
        ax.set_yticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_yticklabels(labels)

        for i in range(len(labels)):
            for j in range(len(labels)):
                val = corr.values[i, j]
                color = 'white' if abs(val) > 0.5 else 'black'
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontsize=9, fontweight='bold')

        plt.colorbar(im, ax=ax)
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
else:
    st.error(f"Missing: {missing}")
