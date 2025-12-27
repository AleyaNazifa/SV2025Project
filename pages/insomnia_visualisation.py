import numpy as np
import pandas as pd
import streamlit as st
from data_loader import get_dataframe_from_session

st.set_page_config(page_title="Visualizations", layout="wide", page_icon="📊")

# Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main .block-container {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 3rem 2rem;
        margin-top: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    
    .viz-section {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border: 2px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .insight-box {
        background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
        border-left: 4px solid #667eea;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Sleep & Academic Performance Visualizations")
st.markdown("**Interactive Analysis Dashboard**")
st.markdown("---")

df = get_dataframe_from_session()
if df is None:
    st.warning("⚠️ No data loaded. Please go to the Home page to load your dataset.")
    st.stop()

# ===== SIDEBAR FILTERS =====
st.sidebar.markdown("### 🎯 Filter Data")

def multiselect_filter(df, label, col):
    if col not in df.columns:
        return df
    options = sorted(df[col].dropna().unique().tolist())
    selected = st.sidebar.multiselect(f"{label}", options, default=options)
    return df[df[col].isin(selected)] if selected else df

df_filtered = df.copy()
df_filtered = multiselect_filter(df_filtered, "👤 Gender", "What is your gender?")
df_filtered = multiselect_filter(df_filtered, "🎂 Age Group", "What is your age group?")
df_filtered = multiselect_filter(df_filtered, "📚 Year of Study", "What is your year of study?")
df_filtered = multiselect_filter(df_filtered, "🏛️ Faculty", "Which faculty are you currently enrolled in?")

st.sidebar.markdown("---")
st.sidebar.info(f"📊 **Showing:** {len(df_filtered)} of {len(df)} responses\n\n**Filtered:** {len(df_filtered)/len(df)*100:.1f}%")

# ===== VIZ 1: Sleep Duration Distribution =====
st.markdown("## 1️⃣ Sleep Duration Distribution")
st.markdown("Understanding how many hours students sleep per night")

if "SleepHours_est" in df_filtered.columns:
    sleep_data = df_filtered["SleepHours_est"].dropna()
    
    # Create bins
    bins = [0, 5, 6, 7, 8, 10]
    labels = ["<5 hours", "5-6 hours", "6-7 hours", "7-8 hours", ">8 hours"]
    sleep_binned = pd.cut(sleep_data, bins=bins, labels=labels, include_lowest=True)
    
    dist_df = sleep_binned.value_counts().reset_index()
    dist_df.columns = ["Category", "Count"]
    dist_df = dist_df.sort_values("Category")
    
    st.vega_lite_chart(
        dist_df,
        {
            "mark": {"type": "bar", "cornerRadiusTopLeft": 10, "cornerRadiusTopRight": 10},
            "encoding": {
                "x": {
                    "field": "Category",
                    "type": "ordinal",
                    "title": "Sleep Duration",
                    "axis": {"labelAngle": -45}
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
        },
        use_container_width=True
    )
    
    avg_sleep = sleep_data.mean()
    st.markdown(f"""
    <div class="insight-box">
        <strong>📌 Key Insight:</strong> Average sleep duration is <strong>{avg_sleep:.2f} hours</strong>. 
        The recommended sleep for adults is 7-9 hours per night.
    </div>
    """, unsafe_allow_html=True)
else:
    st.error("❌ Sleep hours data not available")

st.markdown("---")

# ===== VIZ 2: Sleep Quality vs Insomnia =====
st.markdown("## 2️⃣ Sleep Quality Impact on Insomnia Severity")
st.markdown("Exploring how perceived sleep quality relates to insomnia symptoms")

need = {"SleepQuality_score", "InsomniaSeverity_index"}
if need.issubset(df_filtered.columns):
    plot_df = df_filtered[list(need)].dropna()
    plot_df["SleepQuality_score"] = plot_df["SleepQuality_score"].astype(int)
    
    quality_summary = plot_df.groupby("SleepQuality_score").agg({
        "InsomniaSeverity_index": ["mean", "std", "count"]
    }).reset_index()
    
    quality_summary.columns = ["Quality", "Mean", "Std", "Count"]
    quality_summary["Quality_Label"] = quality_summary["Quality"].map({
        1: "1 (Poor)", 2: "2 (Fair)", 3: "3 (Good)", 4: "4 (V.Good)", 5: "5 (Excellent)"
    })
    
    st.vega_lite_chart(
        quality_summary,
        {
            "layer": [
                {
                    "mark": {"type": "bar", "opacity": 0.7, "cornerRadiusTopLeft": 8, "cornerRadiusTopRight": 8},
                    "encoding": {
                        "x": {"field": "Quality_Label", "type": "ordinal", "title": "Sleep Quality Rating"},
                        "y": {"field": "Mean", "type": "quantitative", "title": "Insomnia Severity Index"},
                        "color": {"value": "#667eea"},
                        "tooltip": [
                            {"field": "Quality_Label", "title": "Quality"},
                            {"field": "Mean", "format": ".2f", "title": "Avg Insomnia"},
                            {"field": "Count", "title": "Students"}
                        ]
                    }
                },
                {
                    "mark": {"type": "point", "filled": True, "size": 100},
                    "encoding": {
                        "x": {"field": "Quality_Label", "type": "ordinal"},
                        "y": {"field": "Mean", "type": "quantitative"},
                        "color": {"value": "#764ba2"}
                    }
                }
            ],
            "width": "container",
            "height": 400
        },
        use_container_width=True
    )
    
    corr = plot_df.corr().iloc[0, 1]
    st.markdown(f"""
    <div class="insight-box">
        <strong>📌 Key Insight:</strong> Correlation coefficient: <strong>{corr:+.3f}</strong>. 
        Lower sleep quality is associated with higher insomnia severity.
    </div>
    """, unsafe_allow_html=True)
else:
    st.error("❌ Required data not available")

st.markdown("---")

# ===== VIZ 3: Insomnia vs Academic Impact Scatter =====
st.markdown("## 3️⃣ Insomnia vs Academic Impact")
st.markdown("Relationship between sleep problems and academic performance impacts")

need = {"InsomniaSeverity_index", "AcademicImpact_index"}
if need.issubset(df_filtered.columns):
    scatter_df = df_filtered[list(need)].dropna()
    
    if len(scatter_df) >= 2:
        # Calculate correlation
        x = scatter_df["InsomniaSeverity_index"].to_numpy()
        y = scatter_df["AcademicImpact_index"].to_numpy()
        corr = np.corrcoef(x, y)[0, 1]
        
        # Create regression line data
        m, b = np.polyfit(x, y, 1)
        line_df = pd.DataFrame({
            "Insomnia": [x.min(), x.max()],
            "Impact_Line": [m*x.min()+b, m*x.max()+b]
        })
        
        st.vega_lite_chart(
            scatter_df,
            {
                "layer": [
                    {
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
                        }
                    }
                ],
                "width": "container",
                "height": 400
            },
            use_container_width=True
        )
        
        st.markdown(f"""
        <div class="insight-box">
            <strong>📌 Key Insight:</strong> Correlation: <strong>{corr:+.3f}</strong>. 
            {'Strong positive correlation - higher insomnia severity predicts greater academic impact.' if corr > 0.5 
            else 'Moderate positive correlation between insomnia and academic difficulties.' if corr > 0.3
            else 'Weak correlation observed.'}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Not enough data points for scatter analysis")
else:
    st.error("❌ Required data not available")

st.markdown("---")

# ===== VIZ 4: Performance by Insomnia Group =====
st.markdown("## 4️⃣ Academic Performance by Insomnia Severity Group")
st.markdown("Comparing academic outcomes across different insomnia severity levels")

need = {"InsomniaSeverity_index", "AcademicPerformance_score"}
if need.issubset(df_filtered.columns):
    perf_df = df_filtered[list(need)].dropna()
    
    def categorize_insomnia(v):
        if v < 1.5: return "Low"
        if v < 3.0: return "Moderate"
        return "High"
    
    perf_df["InsomniaGroup"] = perf_df["InsomniaSeverity_index"].apply(categorize_insomnia)
    
    group_stats = perf_df.groupby("InsomniaGroup").agg({
        "AcademicPerformance_score": ["mean", "count"]
    }).reset_index()
    
    group_stats.columns = ["Group", "Performance", "Count"]
    group_stats["Group"] = pd.Categorical(group_stats["Group"], ["Low", "Moderate", "High"], ordered=True)
    group_stats = group_stats.sort_values("Group")
    
    st.vega_lite_chart(
        group_stats,
        {
            "mark": {"type": "bar", "cornerRadiusTopLeft": 10, "cornerRadiusTopRight": 10},
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
        },
        use_container_width=True
    )
    
    low_perf = group_stats[group_stats["Group"] == "Low"]["Performance"].values[0] if "Low" in group_stats["Group"].values else 0
    high_perf = group_stats[group_stats["Group"] == "High"]["Performance"].values[0] if "High" in group_stats["Group"].values else 0
    diff = low_perf - high_perf
    
    st.markdown(f"""
    <div class="insight-box">
        <strong>📌 Key Insight:</strong> Students with low insomnia score {diff:.2f} points higher on average 
        compared to those with high insomnia severity.
    </div>
    """, unsafe_allow_html=True)
else:
    st.error("❌ Required data not available")

st.markdown("---")

# ===== VIZ 5: Correlation Heatmap =====
st.markdown("## 5️⃣ Comprehensive Correlation Matrix")
st.markdown("Understanding relationships between all key variables")

corr_cols = [
    "SleepHours_est", "SleepQuality_score", "InsomniaSeverity_index",
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
        
        # Shorten labels
        label_map = {
            "SleepHours_est": "Sleep Hrs",
            "SleepQuality_score": "Quality",
            "InsomniaSeverity_index": "Insomnia",
            "AcademicImpact_index": "Impact",
            "Stress_score": "Stress",
            "AcademicPerformance_score": "Performance",
            "DeviceBeforeSleep_score": "Device Use",
            "CaffeineUse_score": "Caffeine",
            "Exercise_score": "Exercise"
        }
        
        corr_melted["Var1_Label"] = corr_melted["Variable1"].map(label_map)
        corr_melted["Var2_Label"] = corr_melted["Variable2"].map(label_map)
        
        st.vega_lite_chart(
            corr_melted,
            {
                "mark": "rect",
                "encoding": {
                    "x": {"field": "Var2_Label", "type": "nominal", "title": None},
                    "y": {"field": "Var1_Label", "type": "nominal", "title": None},
                    "color": {
                        "field": "Correlation",
                        "type": "quantitative",
                        "scale": {"scheme": "redblue", "domain": [-1, 1], "reverse": True},
                        "title": "Correlation"
                    },
                    "tooltip": [
                        {"field": "Var1_Label", "title": "Variable 1"},
                        {"field": "Var2_Label", "title": "Variable 2"},
                        {"field": "Correlation", "format": ".3f", "title": "Correlation"}
                    ]
                },
                "width": "container",
                "height": 500
            },
            use_container_width=True
        )
        
        st.markdown("""
        <div class="insight-box">
            <strong>📌 Key Insight:</strong> The heatmap reveals interconnected relationships. 
            Blue indicates positive correlations, red indicates negative correlations.
            Darker colors represent stronger relationships.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Not enough data after filtering")
else:
    st.error(f"❌ Need at least 3 variables. Available: {len(available_cols)}")

st.markdown("---")
st.success("✅ All visualizations loaded successfully")
