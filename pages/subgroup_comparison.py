"""
Subgroup Comparison Page
Compare metrics across different demographic groups
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from data_loader import get_dataframe_from_session
from styles import apply_global_styles

st.set_page_config(page_title="Subgroup Comparison", layout="wide", page_icon="👥")

# Apply global styles
apply_global_styles()

st.title("👥 Subgroup Comparison Analysis")
st.markdown("**Compare sleep and academic metrics across different demographic groups**")
st.markdown("---")

df = get_dataframe_from_session()
if df is None:
    st.warning("⚠️ No data loaded. Please go to the main app page to load your dataset first.")
    st.stop()

# ===== SIDEBAR: SELECT COMPARISON VARIABLE =====
with st.sidebar:
    st.markdown("### 🎯 Comparison Settings")
    
    compare_by = st.selectbox(
        "Compare by",
        ["What is your gender?", "What is your age group?", "What is your year of study?", 
         "Which faculty are you currently enrolled in?"],
        index=0
    )
    
    st.markdown("---")
    
    metrics_to_show = st.multiselect(
        "Select metrics to display",
        ["InsomniaSeverity_index", "AcademicImpact_index", "SleepHours_est", 
         "SleepQuality_score", "Stress_score", "AcademicPerformance_score"],
        default=["InsomniaSeverity_index", "AcademicImpact_index", "SleepHours_est"]
    )

# ===== COMPARISON TABLE =====
st.markdown("## 📊 Comparison Table")

if compare_by in df.columns and len(metrics_to_show) > 0:
    available_metrics = [m for m in metrics_to_show if m in df.columns]
    
    if len(available_metrics) > 0:
        comparison_df = df.groupby(compare_by)[available_metrics].agg(['mean', 'std', 'count']).reset_index()
        
        st.dataframe(comparison_df, use_container_width=True, height=400)
        
        st.markdown("---")
        
        # ===== VISUALIZATIONS FOR EACH METRIC =====
        st.markdown("## 📈 Visual Comparisons")
        
        for metric in available_metrics:
            st.markdown(f"### {metric}")
            
            metric_data = df[[compare_by, metric]].dropna()
            group_summary = metric_data.groupby(compare_by)[metric].mean().reset_index()
            group_summary.columns = ["Group", "Value"]
            
            st.vega_lite_chart(
                group_summary,
                {
                    "mark": {"type": "bar", "cornerRadiusTopLeft": 10, "cornerRadiusTopRight": 10},
                    "encoding": {
                        "x": {
                            "field": "Group",
                            "type": "nominal",
                            "title": compare_by,
                            "axis": {"labelAngle": -45, "labelFontSize": 11}
                        },
                        "y": {
                            "field": "Value",
                            "type": "quantitative",
                            "title": f"Average {metric}",
                            "axis": {"labelFontSize": 12}
                        },
                        "color": {
                            "field": "Value",
                            "type": "quantitative",
                            "scale": {"scheme": "viridis"},
                            "legend": None
                        },
                        "tooltip": [
                            {"field": "Group", "type": "nominal"},
                            {"field": "Value", "format": ".2f", "title": "Average"}
                        ]
                    },
                    "width": "container",
                    "height": 350
                },
                use_container_width=True
            )
            
            st.markdown("---")
    else:
        st.error("❌ Selected metrics not found in dataset")
else:
    st.error("❌ Cannot perform comparison - check your data")

st.success("✅ Comparison analysis complete")
