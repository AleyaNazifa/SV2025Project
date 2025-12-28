import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from data_loader import get_dataframe_from_session
from styles import apply_global_styles

st.set_page_config(page_title="Subgroup Comparison", layout="wide", page_icon="👥")
apply_global_styles()

st.title("👥 Subgroup Comparison Analysis")
st.markdown("**Compare metrics across demographics**")
st.markdown("---")

df = get_dataframe_from_session()
if df is None:
    st.warning("⚠️ No data. Go to main app first.")
    st.stop()

# SIDEBAR
with st.sidebar:
    st.markdown("### 🎯 Settings")
    
    compare_by = st.selectbox(
        "Compare by",
        ["What is your gender?", "What is your age group?", "What is your year of study?", 
         "Which faculty are you currently enrolled in?"],
        index=0
    )
    
    st.markdown("---")
    
    metrics = st.multiselect(
        "Select metrics",
        ["InsomniaSeverity_index", "AcademicImpact_index", "SleepHours_est", 
         "SleepQuality_score", "Stress_score", "AcademicPerformance_score"],
        default=["InsomniaSeverity_index", "AcademicImpact_index", "SleepHours_est"]
    )

# TABLE
st.markdown("## 📊 Comparison Table")

if compare_by in df.columns and len(metrics) > 0:
    available = [m for m in metrics if m in df.columns]
    
    if len(available) > 0:
        comparison = df.groupby(compare_by)[available].agg(['mean', 'std', 'count']).reset_index()
        st.dataframe(comparison, use_container_width=True, height=400)
        
        st.markdown("---")
        
        # CHARTS
        st.markdown("## 📈 Visual Comparisons")
        
        for metric in available:
            st.markdown(f"### {metric}")
            
            data = df[[compare_by, metric]].dropna()
            summary = data.groupby(compare_by)[metric].mean().reset_index()
            summary.columns = ["Group", "Value"]
            
            st.vega_lite_chart(summary, {
                "mark": {"type": "bar", "cornerRadiusTopLeft": 10, "cornerRadiusTopRight": 10},
                "encoding": {
                    "x": {"field": "Group", "type": "nominal", "title": compare_by, "axis": {"labelAngle": -45}},
                    "y": {"field": "Value", "type": "quantitative", "title": f"Avg {metric}"},
                    "color": {"field": "Value", "type": "quantitative", "scale": {"scheme": "viridis"}, "legend": None},
                    "tooltip": [
                        {"field": "Group", "type": "nominal"},
                        {"field": "Value", "format": ".2f", "title": "Average"}
                    ]
                },
                "width": "container",
                "height": 350
            }, use_container_width=True)
            
            st.markdown("---")
    else:
        st.error("❌ Metrics not found")
else:
    st.error("❌ Cannot compare")

st.success("✅ Comparison complete")
```

---
