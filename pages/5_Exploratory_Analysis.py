from __future__ import annotations

import streamlit as st

from modules.eda import correlation_heatmap, distribution_summary, outcome_scatter_plots, feature_distribution_plots
from modules.preprocessing import load_dataset, prepare_processed_dataset
from utils.helpers import ensure_default_dataset

st.set_page_config(page_title="EDA", layout="wide")

st.title("Exploratory Data Analysis")

try:
    dataset_path = ensure_default_dataset()
    raw = load_dataset(dataset_path)
    cleaned, _ = prepare_processed_dataset(raw)
except Exception as exc:
    st.error(f"EDA data load failed: {exc}")
    st.stop()

st.subheader("Descriptive statistics")
st.dataframe(distribution_summary(cleaned), use_container_width=True)

plots = feature_distribution_plots(cleaned)
fig_keys = ["outcome_pie", "age_distribution", "glucose_distribution", "bmi_distribution", "outcome_by_age"]
for i, key in enumerate(fig_keys):
    st.plotly_chart(plots[key], use_container_width=True)

scatter_plots = outcome_scatter_plots(cleaned)
for feature in ["Glucose", "BMI", "Age", "Pregnancies"]:
    st.plotly_chart(scatter_plots[f"{feature}_vs_outcome"], use_container_width=True)

st.plotly_chart(correlation_heatmap(cleaned), use_container_width=True)

st.markdown("### Meaningful interpretation")
st.markdown(
    """
    - Glucose and BMI are often strongly tied to diabetic outcomes in this dataset.
    - Age and pregnancy history contribute to risk patterns and should be interpreted with clinical context.
    - The heatmap helps identify which health indicators move together and which show stronger relationships with the outcome.
    """
)
