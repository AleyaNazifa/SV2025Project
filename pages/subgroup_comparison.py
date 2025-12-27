import matplotlib.pyplot as plt
import streamlit as st
from data_loader import get_dataframe_from_session

st.title("👥 Subgroup Comparison")
st.markdown("### Compare metrics across different demographics")
st.divider()

df = get_dataframe_from_session()
if df is None:
    st.warning("⚠️ No data loaded. Go to main page first.")
    st.stop()

# Controls
col1, col2 = st.columns(2)

with col1:
    group_col = st.selectbox(
        "📊 Compare by:",
        ["Which faculty are you currently enrolled in?", 
         "What is your year of study?", 
         "What is your age group?",
         "What is your gender?"]
    )

with col2:
    metric = st.selectbox(
        "📈 Metric:",
        ["InsomniaSeverity_index", 
         "AcademicImpact_index", 
         "SleepHours_est", 
         "SleepQuality_score",
         "Stress_score",
         "AcademicPerformance_score"]
    )

if group_col not in df.columns or metric not in df.columns:
    st.error("❌ Selected columns not available")
    st.stop()

plot_df = df[[group_col, metric]].dropna()

if len(plot_df) == 0:
    st.warning("⚠️ No data for this combination")
    st.stop()

means = plot_df.groupby(group_col)[metric].mean().sort_values(ascending=False)
counts = plot_df.groupby(group_col)[metric].count()
std_devs = plot_df.groupby(group_col)[metric].std()

# Visualization
st.markdown("### 📊 Comparison Chart")

metric_names = {
    "InsomniaSeverity_index": "Insomnia Severity",
    "AcademicImpact_index": "Academic Impact",
    "SleepHours_est": "Sleep Hours",
    "SleepQuality_score": "Sleep Quality",
    "Stress_score": "Stress Level",
    "AcademicPerformance_score": "Academic Performance"
}

fig, ax = plt.subplots(figsize=(12, 6))

from matplotlib import cm
colors = cm.viridis(means / means.max())

bars = ax.bar(range(len(means)), means.values, color=colors, edgecolor="black", linewidth=2, alpha=0.8)

for i, (bar, mean_val, count) in enumerate(zip(bars, means.values, counts)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{mean_val:.2f}\n(n={int(count)})',
            ha='center', va='bottom', fontweight='bold', fontsize=9)

ax.set_xticks(range(len(means)))
ax.set_xticklabels([str(label)[:30] for label in means.index], rotation=45, ha="right")
ax.set_title(f"{metric_names.get(metric, metric)} by Group", fontsize=14, fontweight='bold')
ax.set_xlabel(group_col.replace('What is your ', '').replace('Which faculty are you currently enrolled in?', 'Faculty'))
ax.set_ylabel(metric_names.get(metric, metric))
ax.grid(axis='y', alpha=0.3)

overall_mean = means.mean()
ax.axhline(y=overall_mean, color='red', linestyle='--', linewidth=2, label=f'Mean: {overall_mean:.2f}', alpha=0.7)
ax.legend()

plt.tight_layout()
st.pyplot(fig, clear_figure=True)

st.divider()

# Statistics
st.markdown("### 📊 Statistics")

col_a, col_b, col_c = st.columns(3)

with col_a:
    highest_group = means.idxmax()
    highest_value = means.max()
    st.metric("🏆 Highest", f"{highest_value:.2f}", delta=str(highest_group)[:20])

with col_b:
    lowest_group = means.idxmin()
    lowest_value = means.min()
    st.metric("📉 Lowest", f"{lowest_value:.2f}", delta=str(lowest_group)[:20])

with col_c:
    range_val = means.max() - means.min()
    st.metric("📏 Range", f"{range_val:.2f}")

# Table
st.markdown("### 📋 Detailed Table")

stats_df = plot_df.groupby(group_col)[metric].agg(['mean', 'std', 'min', 'max', 'count']).round(2)
stats_df.columns = ['Mean', 'Std Dev', 'Min', 'Max', 'Count']
stats_df = stats_df.sort_values('Mean', ascending=False)

st.dataframe(stats_df, use_container_width=True)

st.info(f"""
💡 **Key Insight:** {str(highest_group)[:40]} has the highest {metric_names.get(metric, metric).lower()} 
at **{highest_value:.2f}**, while {str(lowest_group)[:40]} has the lowest at **{lowest_value:.2f}**
""")
