import numpy as np
import pandas as pd
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from data_loader import get_dataframe_from_session
from styles import apply_global_styles

st.set_page_config(page_title="Visualizations", layout="wide", page_icon="📊")
apply_global_styles()

st.title("📊 Sleep & Academic Performance Visualizations")
st.markdown("**Interactive Analysis Dashboard**")
st.markdown("---")

df = get_dataframe_from_session()
if df is None:
    st.warning("⚠️ No data loaded. Go to main app page first.")
    st.stop()

# FILTERS
with st.sidebar:
    st.markdown("### 🎯 Filter Data")

def multiselect_filter(df, label, col, icon=""):
    if col not in df.columns:
        return df
    options = sorted(df[col].dropna().unique().tolist())
    selected = st.sidebar.multiselect(f"{icon} {label}", options, default=options, key=f"filter_{col}")
    return df[df[col].isin(selected)] if selected else df

df_filtered = df.copy()
df_filtered = multiselect_filter(df_filtered, "Gender", "What is your gender?", "👤")
df_filtered = multiselect_filter(df_filtered, "Age Group", "What is your age group?", "🎂")
df_filtered = multiselect_filter(df_filtered, "Year of Study", "What is your year of study?", "📚")
df_filtered = multiselect_filter(df_filtered, "Faculty", "Which faculty are you currently enrolled in?", "🏛️")

with st.sidebar:
    st.markdown("---")
    st.info(f"""
**📊 Filtered Data**

Showing: {len(df_filtered):,}  
Total: {len(df):,}  
Percent: {len(df_filtered)/len(df)*100:.1f}%
""")

# VIZ 1
st.markdown("## 1️⃣ Sleep Duration Distribution")

if "SleepHours_est" in df_filtered.columns:
    sleep_data = df_filtered["SleepHours_est"].dropna()
    bins = [0, 5, 6, 7, 8, 10]
    labels = ["<5h", "5-6h", "6-7h", "7-8h", ">8h"]
    sleep_binned = pd.cut(sleep_data, bins=bins, labels=labels, include_lowest=True)
    
    dist_df = sleep_binned.value_counts().reset_index()
    dist_df.columns = ["Category", "Count"]
    
    st.vega_lite_chart(dist_df, {
        "mark": {"type": "bar", "cornerRadiusTopLeft": 10, "cornerRadiusTopRight": 10},
        "encoding": {
            "x": {"field": "Category", "type": "ordinal", "title": "Sleep Duration"},
            "y": {"field": "Count", "type": "quantitative", "title": "Students"},
            "color": {"field": "Count", "type": "quantitative", "scale": {"scheme": "purples"}, "legend": None},
            "tooltip": [
                {"field": "Category", "title": "Duration"},
                {"field": "Count", "title": "Students"}
            ]
        },
        "width": "container",
        "height": 400
    }, use_container_width=True)
    
    st.markdown(f"""
    <div class="insight-box">
        <strong>📌 Insight:</strong> Average sleep is <strong>{sleep_data.mean():.2f} hours</strong>. 
        Recommended: 7-9 hours.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# VIZ 2
st.markdown("## 2️⃣ Sleep Quality vs Insomnia")

need = {"SleepQuality_score", "InsomniaSeverity_index"}
if need.issubset(df_filtered.columns):
    plot_df = df_filtered[list(need)].dropna()
    plot_df["SleepQuality_score"] = plot_df["SleepQuality_score"].astype(int)
    
    quality_summary = plot_df.groupby("SleepQuality_score").agg({
        "InsomniaSeverity_index": ["mean", "count"]
    }).reset_index()
    quality_summary.columns = ["Quality", "Mean", "Count"]
    quality_summary["Label"] = quality_summary["Quality"].map({
        1: "1-Poor", 2: "2-Fair", 3: "3-Good", 4: "4-VGood", 5: "5-Excellent"
    })
    
    st.vega_lite_chart(quality_summary, {
        "layer": [
            {
                "mark": {"type": "bar", "opacity": 0.7, "cornerRadiusTopLeft": 8, "cornerRadiusTopRight": 8},
                "encoding": {
                    "x": {"field": "Label", "type": "ordinal", "title": "Sleep Quality"},
                    "y": {"field": "Mean", "type": "quantitative", "title": "Insomnia Severity"},
                    "color": {"value": "#667eea"},
                    "tooltip": [
                        {"field": "Label", "title": "Quality"},
                        {"field": "Mean", "format": ".2f", "title": "Avg Insomnia"},
                        {"field": "Count", "title": "Students"}
                    ]
                }
            },
            {
                "mark": {"type": "point", "filled": True, "size": 100},
                "encoding": {
                    "x": {"field": "Label", "type": "ordinal"},
                    "y": {"field": "Mean", "type": "quantitative"},
                    "color": {"value": "#764ba2"}
                }
            }
        ],
        "width": "container",
        "height": 400
    }, use_container_width=True)
    
    corr = plot_df.corr().iloc[0, 1]
    st.markdown(f"""
    <div class="insight-box">
        <strong>📌 Insight:</strong> Correlation: <strong>{corr:+.3f}</strong>. 
        Lower sleep quality = higher insomnia.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# VIZ 3
st.markdown("## 3️⃣ Insomnia vs Academic Impact")

need = {"InsomniaSeverity_index", "AcademicImpact_index"}
if need.issubset(df_filtered.columns):
    scatter_df = df_filtered[list(need)].dropna()
    
    if len(scatter_df) >= 2:
        x = scatter_df["InsomniaSeverity_index"].to_numpy()
        y = scatter_df["AcademicImpact_index"].to_numpy()
        corr = np.corrcoef(x, y)[0, 1]
        
        st.vega_lite_chart(scatter_df, {
            "mark": {"type": "circle", "opacity": 0.6, "size": 100},
            "encoding": {
                "x": {"field": "InsomniaSeverity_index", "type": "quantitative", "title": "Insomnia Severity", "scale": {"zero": False}},
                "y": {"field": "AcademicImpact_index", "type": "quantitative", "title": "Academic Impact", "scale": {"zero": False}},
                "color": {"field": "AcademicImpact_index", "type": "quantitative", "scale": {"scheme": "redyellowblue", "reverse": True}, "legend": {"title": "Impact"}},
                "tooltip": [
                    {"field": "InsomniaSeverity_index", "format": ".2f", "title": "Insomnia"},
                    {"field": "AcademicImpact_index", "format": ".2f", "title": "Impact"}
                ]
            },
            "width": "container",
            "height": 400
        }, use_container_width=True)
        
        st.markdown(f"""
        <div class="insight-box">
            <strong>📌 Insight:</strong> Correlation: <strong>{corr:+.3f}</strong>. 
            {'Strong positive link' if corr > 0.5 else 'Moderate link' if corr > 0.3 else 'Weak link'}.
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# VIZ 4
st.markdown("## 4️⃣ Performance by Insomnia Group")

need = {"InsomniaSeverity_index", "AcademicPerformance_score"}
if need.issubset(df_filtered.columns):
    perf_df = df_filtered[list(need)].dropna()
    
    def categorize(v):
        if v < 1.5: return "Low"
        if v < 3.0: return "Moderate"
        return "High"
    
    perf_df["Group"] = perf_df["InsomniaSeverity_index"].apply(categorize)
    
    group_stats = perf_df.groupby("Group").agg({
        "AcademicPerformance_score": ["mean", "count"]
    }).reset_index()
    group_stats.columns = ["Group", "Performance", "Count"]
    group_stats["Group"] = pd.Categorical(group_stats["Group"], ["Low", "Moderate", "High"], ordered=True)
    group_stats = group_stats.sort_values("Group")
    
    st.vega_lite_chart(group_stats, {
        "mark": {"type": "bar", "cornerRadiusTopLeft": 10, "cornerRadiusTopRight": 10},
        "encoding": {
            "x": {"field": "Group", "type": "ordinal", "title": "Insomnia Group"},
            "y": {"field": "Performance", "type": "quantitative", "title": "Avg Performance", "scale": {"domain": [0, 5]}},
            "color": {
                "field": "Group",
                "type": "nominal",
                "scale": {"domain": ["Low", "Moderate", "High"], "range": ["#10b981", "#f59e0b", "#ef4444"]},
                "legend": None
            },
            "tooltip": [
                {"field": "Group", "title": "Level"},
                {"field": "Performance", "format": ".2f", "title": "Performance"},
                {"field": "Count", "title": "Students"}
            ]
        },
        "width": "container",
        "height": 400
    }, use_container_width=True)
    
    low = group_stats[group_stats["Group"] == "Low"]["Performance"].values[0] if "Low" in group_stats["Group"].values else 0
    high = group_stats[group_stats["Group"] == "High"]["Performance"].values[0] if "High" in group_stats["Group"].values else 0
    
    st.markdown(f"""
    <div class="insight-box">
        <strong>📌 Insight:</strong> Low insomnia students score {low-high:.2f} points higher.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# VIZ 5
st.markdown("## 5️⃣ Correlation Matrix")

corr_cols = [
    "SleepHours_est", "SleepQuality_score", "InsomniaSeverity_index",
    "AcademicImpact_index", "Stress_score", "AcademicPerformance_score",
    "DeviceBeforeSleep_score", "CaffeineUse_score", "Exercise_score"
]

available = [c for c in corr_cols if c in df_filtered.columns]

if len(available) >= 3:
    corr_df = df_filtered[available].dropna()
    
    if len(corr_df) >= 3:
        corr_matrix = corr_df.corr()
        corr_melted = corr_matrix.reset_index().melt(id_vars="index")
        corr_melted.columns = ["Var1", "Var2", "Correlation"]
        
        label_map = {
            "SleepHours_est": "Sleep Hrs",
            "SleepQuality_score": "Quality",
            "InsomniaSeverity_index": "Insomnia",
            "AcademicImpact_index": "Impact",
            "Stress_score": "Stress",
            "AcademicPerformance_score": "Performance",
            "DeviceBeforeSleep_score": "Device",
            "CaffeineUse_score": "Caffeine",
            "Exercise_score": "Exercise"
        }
        
        corr_melted["V1"] = corr_melted["Var1"].map(label_map)
        corr_melted["V2"] = corr_melted["Var2"].map(label_map)
        
        st.vega_lite_chart(corr_melted, {
            "mark": "rect",
            "encoding": {
                "x": {"field": "V2", "type": "nominal", "title": None},
                "y": {"field": "V1", "type": "nominal", "title": None},
                "color": {
                    "field": "Correlation",
                    "type": "quantitative",
                    "scale": {"scheme": "redblue", "domain": [-1, 1], "reverse": True},
                    "title": "Correlation"
                },
                "tooltip": [
                    {"field": "V1", "title": "Variable 1"},
                    {"field": "V2", "title": "Variable 2"},
                    {"field": "Correlation", "format": ".3f", "title": "Correlation"}
                ]
            },
            "width": "container",
            "height": 500
        }, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>📌 Insight:</strong> Blue = positive correlation, Red = negative. 
            Darker = stronger relationship.
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.success("✅ All visualizations complete")
