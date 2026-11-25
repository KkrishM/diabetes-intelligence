from __future__ import annotations

import streamlit as st

from modules.preprocessing import load_dataset, prepare_processed_dataset
from utils.helpers import ensure_default_dataset
from utils.visualizations import plot_missing_values, plot_outlier_summary

st.set_page_config(page_title="Preprocessing", layout="wide")

st.title("Data Preprocessing and ETL")

uploaded_file = st.file_uploader("Upload a CSV dataset", type=["csv"])
path = ensure_default_dataset() if uploaded_file is None else uploaded_file

if uploaded_file is not None:
    df = load_dataset(uploaded_file)
else:
    df = load_dataset(path)

original = df.copy()
cleaned, summary = prepare_processed_dataset(original)

st.subheader("Original dataset preview")
st.dataframe(original.head(10), use_container_width=True)

st.subheader("Cleaned dataset preview")
st.dataframe(cleaned.head(10), use_container_width=True)

col1, col2 = st.columns(2)
col1.metric("Original rows", len(original))
col2.metric("Cleaned rows", len(cleaned))

st.subheader("Missing values")
missing_before = summary["missing_report"]["before_missing"]
missing_after = summary["missing_report"]["after_missing"]
st.pyplot(plot_missing_values(missing_before, missing_after), use_container_width=True)

st.subheader("Duplicate and outlier summary")
col1, col2, col3 = st.columns(3)
col1.metric("Before duplicates", summary["missing_report"]["before_duplicates"])
col2.metric("After duplicates", summary["missing_report"]["after_duplicates"])
col3.metric("Outlier checks", sum(summary["outlier_summary"].values()))

st.pyplot(plot_outlier_summary(summary["outlier_summary"]), use_container_width=True)

st.subheader("Transformation summary")
transformation_summary = {
    "Columns validated": list(original.columns),
    "Medical zero values converted to missing": [
        "Glucose",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "BMI",
    ],
    "Duplicate rows removed": summary["missing_report"]["before_duplicates"],
    "Missing values imputed using median": True,
    "Outcome validated as binary": True,
}
st.json(transformation_summary)

st.success("ETL completed successfully using a reproducible preprocessing pipeline.")
