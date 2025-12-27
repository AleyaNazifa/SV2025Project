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
    
    .viz-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .control-panel {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .stSelectbox > label {
        font-weight: 600 !important;
        color: #2d3748 !important;
        font-size: 1.1rem !important;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

st.title("👥 Subgroup Comparison")
st.caption("🔍 Compare insomnia severity and academic impact across different student demographics")

df = get_dataframe_from_session()
if df is None:
    st.warning("⚠️ No data loaded yet. Go to the main page to load data.")
    st.stop()

# Control panel
st.markdown('<div class="control-panel">', unsafe_allow_html=True)
st.markdown("### 🎛️ Analysis Configuration")

col1, col2 = st.columns(2)

with col1:
    group_col = st.selectbox(
        "📊 Compare groups by:",
        ["Which faculty are you currently enrolled in?", 
         "What is your year of study?", 
         "What is your age group?",
         "What is your gender?"],
        help="Select the demographic variable to compare"
    )

with col2:
    metric = st.selectbox(
        "📈 Metric to analyze:",
        ["InsomniaSeverity_index", 
         "AcademicImpact_index", 
         "SleepHours_est", 
         "SleepQuality_score",
         "Stress_score",
         "AcademicPerformance_score"],
        help="Select the metric to compare across groups"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Check if columns exist
if group_col not in df.columns or metric not in df.columns:
    st.error("❌ Selected columns are not available in the dataset.")
    st.stop()

# Prepare data
plot_df = df[[group_col, metric]].dropna()

if len(plot_df) == 0:
    st.warning("⚠️ No data available for the selected combination.")
    st.stop()

means = plot_df.groupby(group_col)[metric].mean().sort_values(ascending=False)
counts = plot_df.groupby(group_col)[metric].count()
std_devs = plot_df.groupby(group_col)[metric].std()

# Visualization
st.markdown('<div class="viz-container">', unsafe_allow_html=True)

# Display metric name mapping
metric_names = {
    "InsomniaSeverity_index": "Insomnia Severity Index",
    "AcademicImpact_index": "Academic Impact Index",
    "SleepHours_est": "Estimated Sleep Hours",
    "SleepQuality_score": "Sleep Quality Score",
    "Stress_score": "Stress Level Score",
    "AcademicPerformance_score": "Academic Performance Score"
}

st.subheader(f"📊 {metric_names.get(metric, metric)} by {group_col.replace('What is your ', '').replace('Which faculty are you currently enrolled in?', 'Faculty')}")

fig, ax = plt.subplots(figsize=(12, 6))

# Create gradient colors based on values
from matplotlib import cm
colors = cm.viridis(means / means.max())

bars = ax.bar(range(len(means)), means.values, color=colors, edgecolor="black", linewidth=2, alpha=0.8)

# Add value labels on bars with counts
for i, (bar, mean_val, count, std) in enumerate(zip(bars, means.values, counts, std_devs)):
    height = bar.get_height()
    label_text = f'{mean_val:.2f}\n(n={int(count)})'
    ax.text(bar.get_x() + bar.get_width()/2., height,
            label_text,
            ha='center', va='bottom', fontweight='bold', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))

ax.set_xticks(range(len(means)))
ax.set_xticklabels([str(label)[:30] for label in means.index], rotation=45, ha="right", fontsize=10)
ax.set_title(f"Mean {metric_names.get(metric, metric)} by Group", fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel(group_col.replace('What is your ', '').replace('Which faculty are you currently enrolled in?', 'Faculty'), 
              fontsize=12, fontweight='bold')
ax.set_ylabel(f"Mean {metric_names.get(metric, metric)}", fontsize=12, fontweight='bold')

# Add grid for easier reading
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('white')

# Add a horizontal line for the overall mean
overall_mean = means.mean()
ax.axhline(y=overall_mean, color='red', linestyle='--', linewidth=2, 
           label=f'Overall Mean: {overall_mean:.2f}', alpha=0.7)
ax.legend(fontsize=11, loc='best')

plt.tight_layout()
st.pyplot(fig, clear_figure=True)

st.markdown('</div>', unsafe_allow_html=True)

# Statistics and insights
st.markdown('<div class="control-panel">', unsafe_allow_html=True)
st.markdown("### 📊 Detailed Statistics")

col_a, col_b, col_c = st.columns(3)

with col_a:
    highest_group = means.idxmax()
    highest_value = means.max()
    st.markdown(f"""
    <div style='background: #4ade80; color: white; padding: 1rem; border-radius: 10px; text-align: center;'>
        <h4 style='margin: 0; color: white;'>🏆 Highest</h4>
        <p style='margin: 0.5rem 0; font-size: 0.9rem;'>{str(highest_group)[:30]}</p>
        <p style='margin: 0; font-size: 1.5rem; font-weight: bold;'>{highest_value:.2f}</p>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    lowest_group = means.idxmin()
    lowest_value = means.min()
    st.markdown(f"""
    <div style='background: #60a5fa; color: white; padding: 1rem; border-radius: 10px; text-align: center;'>
        <h4 style='margin: 0; color: white;'>📉 Lowest</h4>
        <p style='margin: 0.5rem 0; font-size: 0.9rem;'>{str(lowest_group)[:30]}</p>
        <p style='margin: 0; font-size: 1.5rem; font-weight: bold;'>{lowest_value:.2f}</p>
    </div>
    """, unsafe_allow_html=True)

with col_c:
    range_val = means.max() - means.min()
    st.markdown(f"""
    <div style='background: #a78bfa; color: white; padding: 1rem; border-radius: 10px; text-align: center;'>
        <h4 style='margin: 0; color: white;'>📏 Range</h4>
        <p style='margin: 0.5rem 0; font-size: 0.9rem;'>Max - Min</p>
        <p style='margin: 0; font-size: 1.5rem; font-weight: bold;'>{range_val:.2f}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Detailed table
st.markdown('<div class="control-panel">', unsafe_allow_html=True)
st.markdown("### 📋 Complete Statistics Table")

stats_df = plot_df.groupby(group_col)[metric].agg(['mean', 'std', 'min', 'max', 'count']).round(2)
stats_df.columns = ['Mean', 'Std Dev', 'Min', 'Max', 'Count']
stats_df = stats_df.sort_values('Mean', ascending=False)

st.dataframe(stats_df, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Insights
st.markdown(f"""
<div class="insight-box">
    <h3 style='margin-top: 0; color: white;'>💡 Key Insights</h3>
    <ul>
        <li><strong>{str(highest_group)[:40]}</strong> has the highest mean {metric_names.get(metric, metric).lower()} at <strong>{highest_value:.2f}</strong></li>
        <li><strong>{str(lowest_group)[:40]}</strong> has the lowest mean at <strong>{lowest_value:.2f}</strong></li>
        <li>The difference between highest and lowest groups is <strong>{range_val:.2f}</strong></li>
        <li>Total sample size across all groups: <strong>{int(counts.sum())}</strong> respondents</li>
    </ul>
</div>
""", unsafe_allow_html=True)
