import matplotlib.pyplot as plt
import streamlit as st
from data_loader import get_dataframe_from_session

st.title("Subgroup Comparison")
st.caption("Compare insomnia severity and academic impact across subgroups (creativity & innovation).")

df = get_dataframe_from_session()
if df is None:
    st.warning("No data loaded yet. Go to the main page to load data.")
    st.stop()

group_col = st.selectbox(
    "Compare by",
    ["Which faculty are you currently enrolled in?", "What is your year of study?", "What is your age group?"],
)

metric = st.selectbox(
    "Metric",
    ["InsomniaSeverity_index", "AcademicImpact_index", "SleepHours_est", "SleepQuality_score"],
)

if group_col not in df.columns or metric not in df.columns:
    st.error("Selected columns not available in the dataset.")
    st.stop()

plot_df = df[[group_col, metric]].dropna()
means = plot_df.groupby(group_col)[metric].mean().sort_values(ascending=False)

fig = plt.figure(figsize=(9, 5))
plt.bar(means.index.astype(str), means.values, edgecolor="black")
plt.xticks(rotation=45, ha="right")
plt.title(f"Mean {metric} by {group_col}")
plt.xlabel(group_col)
plt.ylabel(f"Mean {metric}")
plt.tight_layout()
st.pyplot(fig, clear_figure=True)
