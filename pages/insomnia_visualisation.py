"""
Interactive Visualizations Page
5 comprehensive charts with demographic filters
"""

import numpy as np
import pandas as pd
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from data_loader import get_dataframe_from_session
from styles import apply_styles

st.set_page_config(page_title="Visualizations", layout="wide", page_icon="📊")
apply_styles()

st.title("📊 Sleep & Academic Performance Visualizations")
st.markdown("**Interactive Analysis with Demographic Filters**")
st.markdown("---")

# Load data from session
df = get_dataframe_from_session()
if df is None:
    st.warning("⚠️ No data loaded. Please go to the main app page to load your dataset first.")
    st.stop()

# ========== SIDEBAR FILTERS ==========
with st.sidebar:
    st.markdown("### 🎯 Filter Data")
    st.caption("Select specific groups to analyze")

def create_filter(df, label, column, icon=""):
    """Create multiselect filter for a column"""
    if column not in df.columns:
        return df
    
    options = sorted(df[column].dropna().unique().tolist())
    selected = st.sidebar.multiselect(
        f"{icon} {label}",
        options=options,
        default=options,
        key=f"filter_{column}"
    )
    
    if selected:
        return df[df[column].isin(selected)]
    return df

# Apply filters
df_filtered = df.copy()
df_filtered = create_filter(df_filtered, "Gender", "What is your gender?", "👤")
df_filtered = create_filter(df_filtered, "Age Group", "What is your age group?", "🎂")
df_filtered = create_filter(df_filtered, "Year of Study", "What is your year of study?", "📚")
df_filtered = create_filter(df_filtered, "Faculty", "Which faculty are you currently enrolled in?", "🏛️")

# Filter summary
with st.sidebar:
    st.markdown("---")
    st.info(f"""
**📊 Filtered Dataset**

**Showing:** {len(df_filtered):,} responses  
**Total:** {len(df):,} responses  
**Percentage:** {len(df_filtered)/len(df)*100:.1f}%
""")

# ========== VISUALIZATION 1: Sleep Duration ==========
st.markdown("## 1️⃣ Sleep Duration Distribution")
st.markdown("How many hours do students sleep per night?")

if "SleepHours_est" in df_filtered.columns:
    sleep_data = df_filtered["SleepHours_est"].dropna()
    
    # Create bins
    bins = [0, 5, 6, 7, 8, 10]
    labels = ["<5 hours", "5-6 hours", "6-7 hours", "7-8 hours", ">8 hours"]
    sleep_binned = pd.cut(sleep_data, bins=bins, labels=labels, include_lowest=True)
    
    dist_df = sleep_binned.value_counts().reset_index()
    dist_df.columns = ["Category", "Count"]
    dist_df = dist_df.sort_values("Category")
    
    st.vega_lite_chart(dist_df, {
        "mark": {
            "type": "bar", 
            "cornerRadiusTopLeft": 10, 
            "cornerRadiusTopRight": 10
        },
        "encoding": {
            "x": {
                "field": "Category", 
                "type": "ordinal", 
                "title": "Sleep Duration"
            },
            "y": {
                "field": "Count", 
                "type": "quantitative", 
                "title": "Number of Students"
            },
            "color": {
                "field": "Count", 
                "type": "quantitative", 
                "scale": {"scheme": "purples"}, 
                "legend": None
            },
            "tooltip": [
                {"field": "Category", "type": "nominal", "title": "Duration"},
                {"field": "Count", "type": "quantitative", "title": "Students"}
            ]
        },
        "width": "container",
        "height": 400
    }, use_container_width=True)
    
    avg_sleep = sleep_data.mean()
    st.markdown(f"""
    <div class="insight-box">
        <p><strong>📌 Key Insight:</strong> Average sleep duration is <strong>{avg_sleep:.2f} hours</strong>. 
        The recommended sleep for adults is <strong>7-9 hours</strong> per night.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.error("❌ Sleep hours data not available in dataset")

st.markdown("---")

# ========== VISUALIZATION 2: Sleep Quality vs Insomnia ==========
st.markdown("## 2️⃣ Sleep Quality Impact on Insomnia Severity")
st.markdown("How does perceived sleep quality relate to insomnia symptoms?")

need = {"SleepQuality_score", "InsomniaSeverity_index"}
if need.issubset(df_filtered.columns):
    plot_df = df_filtered[list(need)].dropna()
    plot_df["SleepQuality_score"] = plot_df["SleepQuality_score"].astype(int)
    
    quality_summary = plot_df.groupby("SleepQuality_score").agg({
        "InsomniaSeverity_index": ["mean", "count"]
    }).reset_index()
    quality_summary.columns = ["Quality", "Mean", "Count"]
    quality_summary["Label"] = quality_summary["Quality"].map({
        1: "1 (Poor)", 
        2: "2 (Fair)", 
        3: "3 (Good)", 
        4: "4 (Very Good)", 
        5: "5 (Excellent)"
    })
    
    st.vega_lite_chart(quality_summary, {
        "layer": [
            {
                "mark": {
                    "type": "bar", 
                    "opacity": 0.7, 
                    "cornerRadiusTopLeft": 8, 
                    "cornerRadiusTopRight": 8
                },
                "encoding": {
                    "x": {
                        "field": "Label", 
                        "type": "ordinal", 
                        "title": "Sleep Quality Rating"
                    },
                    "y": {
                        "field": "Mean", 
                        "type": "quantitative", 
                        "title": "Average Insomnia Severity"
                    },
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
        <p><strong>📌 Key Insight:</strong> Correlation coefficient is <strong>{corr:+.3f}</strong>. 
        Lower sleep quality is associated with higher insomnia severity.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.error("❌ Required columns not found in dataset")

st.markdown("---")

# ========== VISUALIZATION 3: Insomnia vs Academic Impact ==========
st.markdown("## 3️⃣ Insomnia vs Academic Impact")
st.markdown("Relationship between sleep problems and academic performance")

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
                "x": {
                    "field": "InsomniaSeverity_index", 
                    "type": "quantitative", 
                    "title": "Insomnia Severity Index",
                    "scale": {"zero": False}
                },
                "y": {
                    "field": "AcademicImpact_index", 
                    "type": "quantitative", 
                    "title": "Academic Impact Index",
                    "scale": {"zero": False}
                },
                "color": {
                    "field": "AcademicImpact_index", 
                    "type": "quantitative", 
                    "scale": {"scheme": "redyellowblue", "reverse": True}, 
                    "legend": {"title": "Impact Level"}
                },
                "tooltip": [
                    {"field": "InsomniaSeverity_index", "format": ".2f", "title": "Insomnia"},
                    {"field": "AcademicImpact_index", "format": ".2f", "title": "Impact"}
                ]
            },
            "width": "container",
            "height": 400
        }, use_container_width=True)
        
        interpretation = (
            "Strong positive correlation - higher insomnia severity predicts greater academic impact." 
            if corr > 0.5 
            else "Moderate positive correlation between insomnia and academic difficulties." 
            if corr > 0.3 
            else "Weak correlation observed between variables."
        )
        
        st.markdown(f"""
        <div class="insight-box">
            <p><strong>📌 Key Insight:</strong> Correlation is <strong>{corr:+.3f}</strong>. {interpretation}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Not enough data points for scatter analysis after filtering")
else:
    st.error("❌ Required columns not found in dataset")

st.markdown("---")

# ========== VISUALIZATION 4: Performance by Group ==========
st.markdown("## 4️⃣ Academic Performance by Insomnia Severity")
st.markdown("Comparing outcomes across different insomnia levels")

need = {"InsomniaSeverity_index", "AcademicPerformance_score"}
if need.issubset(df_filtered.columns):
    perf_df = df_filtered[list(need)].dropna()
    
    def categorize_insomnia(value):
        if value < 1.5:
            return "Low"
        elif value < 3.0:
            return "Moderate"
        else:
            return "High"
    
    perf_df["InsomniaGroup"] = perf_df["InsomniaSeverity_index"].apply(categorize_insomnia)
    
    group_stats = perf_df.groupby("InsomniaGroup").agg({
        "AcademicPerformance_score": ["mean", "count"]
    }).reset_index()
    group_stats.columns = ["Group", "Performance", "Count"]
    group_stats["Group"] = pd.Categorical(
        group_stats["Group"], 
        ["Low", "Moderate", "High"], 
        ordered=True
    )
    group_stats = group_stats.sort_values("Group")
    
    st.vega_lite_chart(group_stats, {
        "mark": {
            "type": "bar", 
            "cornerRadiusTopLeft": 10, 
            "cornerRadiusTopRight": 10
        },
        "encoding": {
            "x": {
                "field": "Group", 
                "type": "ordinal", 
                "title": "Insomnia Severity Group"
            },
            "y": {
                "field": "Performance", 
                "type": "quantitative", 
                "title": "Average Academic Performance Score",
                "scale": {"domain": [0, 5]}
            },
            "color": {
                "field": "Group",
                "type": "nominal",
                "scale": {
                    "domain": ["Low", "Moderate", "High"],
                    "range": ["#10b981", "#f59e0b", "#ef4444"]
                },
                "legend": None
            },
            "tooltip": [
                {"field": "Group", "title": "Insomnia Level"},
                {"field": "Performance", "format": ".2f", "title": "Avg Performance"},
                {"field": "Count", "title": "Students"}
            ]
        },
        "width": "container",
        "height": 400
    }, use_container_width=True)
    
    low_perf = group_stats[group_stats["Group"] == "Low"]["Performance"].values[0] if "Low" in group_stats["Group"].values else 0
    high_perf = group_stats[group_stats["Group"] == "High"]["Performance"].values[0] if "High" in group_stats["Group"].values else 0
    diff = low_perf - high_perf
    
    st.markdown(f"""
    <div class="insight-box">
        <p><strong>📌 Key Insight:</strong> Students with low insomnia score <strong>{diff:.2f} points higher</strong> 
        on average compared to those with high insomnia severity.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.error("❌ Required columns not found in dataset")

st.markdown("---")

# ========== VISUALIZATION 5: Correlation Matrix ==========
st.markdown("## 5️⃣ Comprehensive Correlation Matrix")
st.markdown("Understanding relationships between all key variables")

corr_cols = ["SleepHours_est", "SleepQuality_score", "InsomniaSeverity_index",
"AcademicImpact_index", "Stress_score", "AcademicPerformance_score",
"DeviceBeforeSleep_score", "CaffeineUse_score", "Exercise_score"
]
available_cols = [c for c in corr_cols if c in df_filtered.columns]
if len(available_cols) >= 3:
corr_df = df_filtered[available_cols].dropna()
if len(corr_df) >= 3:
    corr_matrix = corr_df.corr()
    
    # Reshape for heatmap
    corr_melted = corr_matrix.reset_index().melt(id_vars="index")
    corr_melted.columns = ["Variable1", "Variable2", "Correlation"]
    
    # Shorten labels for readability
    label_map = {
        "SleepHours_est": "Sleep Hours",
        "SleepQuality_score": "Sleep Quality",
        "InsomniaSeverity_index": "Insomnia",
        "AcademicImpact_index": "Academic Impact",
        "Stress_score": "Stress",
        "AcademicPerformance_score": "Performance",
        "DeviceBeforeSleep_score": "Device Use",
        "CaffeineUse_score": "Caffeine",
        "Exercise_score": "Exercise"
    }
    
    corr_melted["Var1_Short"] = corr_melted["Variable1"].map(label_map)
    corr_melted["Var2_Short"] = corr_melted["Variable2"].map(label_map)
    
    st.vega_lite_chart(corr_melted, {
        "mark": "rect",
        "encoding": {
            "x": {
                "field": "Var2_Short", 
                "type": "nominal", 
                "title": None
            },
            "y": {
                "field": "Var1_Short", 
                "type": "nominal", 
                "title": None
            },
            "color": {
                "field": "Correlation",
                "type": "quantitative",
                "scale": {
                    "scheme": "redblue", 
                    "domain": [-1, 1], 
                    "reverse": True
                },
                "title": "Correlation"
            },
            "tooltip": [
                {"field": "Var1_Short", "title": "Variable 1"},
                {"field": "Var2_Short", "title": "Variable 2"},
                {"field": "Correlation", "format": ".3f", "title": "Correlation"}
            ]
        },
        "width": "container",
        "height": 500
    }, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        <p><strong>📌 Key Insight:</strong> The heatmap reveals interconnected relationships. 
        <strong>Blue</strong> indicates positive correlations, <strong>red</strong> indicates negative correlations. 
        Darker colors represent stronger relationships.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Not enough data after filtering for correlation analysis")
else:
st.error(f"❌ Need at least 3 variables for correlation. Available: {len(available_cols)}")
st.markdown("---")
st.success("✅ All visualizations loaded successfully!")
