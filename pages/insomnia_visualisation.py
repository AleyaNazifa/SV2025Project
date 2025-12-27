import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from data_loader import get_dataframe_from_session

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    h1 {
        color: #ffffff !important;
        font-size: 3rem !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .stCaption {
        color: #f0f0f0 !important;
        font-size: 1.1rem !important;
    }
    
    h2, h3 {
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .viz-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .filter-info {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
    }
    
    .stMultiSelect > label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .stDivider {
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Insomnia Visualisation")
st.caption("🔬 Core scientific visualizations using 5 different techniques")

df = get_dataframe_from_session()
if df is None:
    st.warning("⚠️ No data loaded yet. Go to the main page to load data.")
    st.stop()

st.sidebar.markdown("### 🎯 Data Filters")
st.sidebar.markdown("Use the filters below to focus your analysis:")

def multiselect_filter(df, label, col):
    if col not in df.columns:
        return df
    options = sorted(df[col].dropna().unique().tolist())
    selected = st.sidebar.multiselect(f"🔍 {label}", options, default=options)
    return df[df[col].isin(selected)] if selected else df

df_f = df.copy()
df_f = multiselect_filter(df_f, "Gender", "What is your gender?")
df_f = multiselect_filter(df_f, "Age Group", "What is your age group?")
df_f = multiselect_filter(df_f, "Year of Study", "What is your year of study?")
df_f = multiselect_filter(df_f, "Faculty", "Which faculty are you currently enrolled in?")

# Filter info display
st.markdown(f"""
<div class="filter-info">
    <strong>📊 Filtered Dataset:</strong> {len(df_f)} rows out of {len(df)} total ({len(df_f)/len(df)*100:.1f}%)
</div>
""", unsafe_allow_html=True)

# Set matplotlib style
plt.style.use('seaborn-v0_8-darkgrid')

# Visualization 1
st.markdown('<div class="viz-container">', unsafe_allow_html=True)
st.subheader("1️⃣ Distribution of Estimated Sleep Duration")
st.caption("Histogram showing how sleep hours are distributed across respondents")

if "SleepHours_est" in df_f.columns:
    s = df_f["SleepHours_est"].dropna()
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Beautiful histogram with gradient colors
    n, bins, patches = ax.hist(s, bins=[4,5,6,7,8,9], edgecolor="white", linewidth=2)
    
    # Color gradient for bars
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(patches)))
    for patch, color in zip(patches, colors):
        patch.set_facecolor(color)
    
    ax.set_title("Distribution of Estimated Sleep Duration", fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel("Estimated Sleep Hours (category midpoint)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Number of Respondents", fontsize=12, fontweight='bold')
    ax.set_xticks([4.5, 5.5, 7.5, 8.5])
    ax.set_xticklabels(["<5h", "5-6h", "7-8h", ">8h"])
    ax.grid(axis='y', alpha=0.3)
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    
    st.pyplot(fig, clear_figure=True)
    
    # Add interpretation
    most_common = s.mode().values[0] if len(s.mode()) > 0 else "N/A"
    st.info(f"💡 **Insight:** Most common sleep duration category is around {most_common:.1f} hours")
else:
    st.error("❌ Missing: SleepHours_est column")

st.markdown('</div>', unsafe_allow_html=True)

# Visualization 2
st.markdown('<div class="viz-container">', unsafe_allow_html=True)
st.subheader("2️⃣ Insomnia Severity by Sleep Quality")
st.caption("Boxplot revealing the relationship between sleep quality ratings and insomnia severity")

need = {"SleepQuality_score", "InsomniaSeverity_index"}
if need.issubset(df_f.columns):
    plot_df = df_f[list(need)].dropna()
    plot_df["SleepQuality_score"] = plot_df["SleepQuality_score"].astype(int)

    levels = sorted(plot_df["SleepQuality_score"].unique())
    data = [plot_df.loc[plot_df["SleepQuality_score"] == lv, "InsomniaSeverity_index"].values for lv in levels]

    fig, ax = plt.subplots(figsize=(10, 5))
    
    bp = ax.boxplot(data, labels=levels, showmeans=True, patch_artist=True,
                    boxprops=dict(facecolor='#667eea', alpha=0.7),
                    medianprops=dict(color='red', linewidth=2),
                    meanprops=dict(marker='D', markerfacecolor='orange', markersize=8),
                    whiskerprops=dict(linewidth=1.5),
                    capprops=dict(linewidth=1.5))
    
    ax.set_title("Insomnia Severity by Self-Rated Sleep Quality", fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel("Sleep Quality Score (1=Poor, 5=Excellent)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Insomnia Severity Index (0–4)", fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    
    st.pyplot(fig, clear_figure=True)
    
    # Add interpretation
    st.info("💡 **Insight:** Lower sleep quality scores typically show higher insomnia severity (red line = median, orange diamond = mean)")
else:
    st.error(f"❌ Missing columns: {sorted(list(need - set(df_f.columns)))}")

st.markdown('</div>', unsafe_allow_html=True)

# Visualization 3
st.markdown('<div class="viz-container">', unsafe_allow_html=True)
st.subheader("3️⃣ Insomnia Severity vs Academic Impact")
st.caption("Scatter plot with trendline showing correlation between insomnia and academic performance")

need = {"InsomniaSeverity_index", "AcademicImpact_index"}
if need.issubset(df_f.columns):
    plot_df = df_f[list(need)].dropna()
    x = plot_df["InsomniaSeverity_index"].to_numpy()
    y = plot_df["AcademicImpact_index"].to_numpy()

    if len(x) >= 2:
        m, b = np.polyfit(x, y, 1)
        r = np.corrcoef(x, y)[0, 1]

        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Scatter plot with color gradient based on density
        scatter = ax.scatter(x, y, alpha=0.6, s=100, c=y, cmap='RdYlBu_r', 
                           edgecolors="black", linewidths=0.5)
        
        # Trendline
        ax.plot([x.min(), x.max()], [m*x.min()+b, m*x.max()+b], 
               'r--', linewidth=3, label=f'Trendline (r={r:.3f})')
        
        ax.set_title("Insomnia Severity vs Academic Impact", fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel("Insomnia Severity Index (0–4)", fontsize=12, fontweight='bold')
        ax.set_ylabel("Academic Impact Index (0–4)", fontsize=12, fontweight='bold')
        ax.legend(fontsize=10, loc='upper left')
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('white')
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Academic Impact', fontsize=10)
        
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)

        # Correlation interpretation
        if r > 0.5:
            strength = "strong positive"
        elif r > 0.3:
            strength = "moderate positive"
        elif r > -0.3:
            strength = "weak"
        elif r > -0.5:
            strength = "moderate negative"
        else:
            strength = "strong negative"
        
        st.info(f"💡 **Insight:** Pearson correlation coefficient is **{r:.3f}**, indicating a **{strength}** relationship")
    else:
        st.warning("⚠️ Not enough filtered data points to compute trendline.")
else:
    st.error(f"❌ Missing columns: {sorted(list(need - set(df_f.columns)))}")

st.markdown('</div>', unsafe_allow_html=True)

# Visualization 4
st.markdown('<div class="viz-container">', unsafe_allow_html=True)
st.subheader("4️⃣ Academic Performance by Insomnia Severity Group")
st.caption("Bar chart comparing mean academic performance across insomnia severity categories")

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

    fig, ax = plt.subplots(figsize=(10, 5))
    
    colors = ['#4ade80', '#fbbf24', '#ef4444']  # Green, Yellow, Red
    bars = ax.bar(means.index, means.values, color=colors, edgecolor="black", linewidth=2, alpha=0.8)
    
    # Add value labels on bars
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}\n(n={int(count)})',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    ax.set_title("Mean Academic Performance by Insomnia Severity Group", fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel("Insomnia Severity Group", fontsize=12, fontweight='bold')
    ax.set_ylabel("Mean Academic Performance Score (1–5)", fontsize=12, fontweight='bold')
    ax.set_ylim(0, max(means.values) * 1.2)
    ax.grid(axis='y', alpha=0.3)
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    
    st.pyplot(fig, clear_figure=True)
    
    st.info(f"💡 **Insight:** Group sizes - {', '.join([f'{k}: {int(v)}' for k, v in counts.dropna().items()])}")
else:
    st.error(f"❌ Missing columns: {sorted(list(need - set(df_f.columns)))}")

st.markdown('</div>', unsafe_allow_html=True)

# Visualization 5
st.markdown('<div class="viz-container">', unsafe_allow_html=True)
st.subheader("5️⃣ Correlation Heatmap")
st.caption("Comprehensive correlation matrix showing relationships between all key variables")

corr_cols = [
    "SleepHours_est", "SleepQuality_score", "InsomniaSeverity_index",
    "AcademicImpact_index", "Stress_score", "AcademicPerformance_score",
    "DeviceBeforeSleep_score", "CaffeineUse_score", "Exercise_score"
]

missing = [c for c in corr_cols if c not in df_f.columns]
if missing:
    st.error(f"❌ Missing columns for heatmap: {missing}")
else:
    corr_df = df_f[corr_cols].dropna()
    if len(corr_df) < 3:
        st.warning("⚠️ Not enough filtered data rows for stable correlation matrix.")
    else:
        corr = corr_df.corr(numeric_only=True)

        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Beautiful heatmap with diverging colormap
        im = ax.imshow(corr.values, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
        
        ax.set_title("Correlation Heatmap: Sleep, Stress, Academic Variables", 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Shortened labels for better display
        short_labels = [
            "Sleep Hrs", "Sleep Qual", "Insomnia",
            "Acad Impact", "Stress", "Acad Perf",
            "Device Use", "Caffeine", "Exercise"
        ]
        
        ax.set_xticks(range(len(corr_cols)))
        ax.set_yticks(range(len(corr_cols)))
        ax.set_xticklabels(short_labels, rotation=45, ha="right", fontsize=10)
        ax.set_yticklabels(short_labels, fontsize=10)

        # Add correlation values as text
        for i in range(len(corr_cols)):
            for j in range(len(corr_cols)):
                val = corr.values[i, j]
                color = 'white' if abs(val) > 0.5 else 'black'
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", 
                       fontsize=9, fontweight='bold', color=color)

        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Correlation Coefficient', fontsize=11, fontweight='bold')
        
        fig.patch.set_facecolor('white')
        plt.tight_layout()
        
        st.pyplot(fig, clear_figure=True)
        
        st.info("💡 **Insight:** Red indicates negative correlation, Blue indicates positive correlation. Darker colors show stronger relationships.")

st.markdown('</div>', unsafe_allow_html=True)
