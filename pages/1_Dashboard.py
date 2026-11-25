from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from modules.preprocessing import load_dataset, prepare_processed_dataset
from utils.helpers import ensure_default_dataset

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("Dashboard Overview")

try:
    dataset_path = ensure_default_dataset()
    df = load_dataset(dataset_path)
    cleaned, _ = prepare_processed_dataset(df)
except Exception as exc:
    st.error(f"Unable to load the dataset: {exc}")
    st.stop()

n_records = len(cleaned)
healthy = int((cleaned["Outcome"] == 0).sum())
positive = int((cleaned["Outcome"] == 1).sum())
percentage = round((positive / n_records) * 100, 2) if n_records else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Patient Records", n_records)
col2.metric("Diabetic Patients", positive)
col3.metric("Non-Diabetic Patients", healthy)
col4.metric("Diabetes %", f"{percentage}%")
col5.metric("Avg Glucose", round(cleaned["Glucose"].mean(), 2))

st.markdown("---")

col1, col2, col3 = st.columns(3)
col1.metric("Avg BMI", round(cleaned["BMI"].mean(), 2))
col2.metric("Avg Age", round(cleaned["Age"].mean(), 2))
col3.metric("Avg Blood Pressure", round(cleaned["BloodPressure"].mean(), 2))

st.subheader("Distribution and relationship charts")
left, right = st.columns(2)
left.plotly_chart(px.pie(cleaned, names="Outcome", title="Diabetes Distribution", hole=0.45), use_container_width=True)
right.plotly_chart(px.histogram(cleaned, x="Age", nbins=25, title="Age Distribution"), use_container_width=True)

left.plotly_chart(px.histogram(cleaned, x="Glucose", nbins=25, title="Glucose Distribution"), use_container_width=True)
right.plotly_chart(px.histogram(cleaned, x="BMI", nbins=25, title="BMI Distribution"), use_container_width=True)

age_bins = pd.cut(cleaned["Age"], bins=[0, 20, 30, 40, 50, 60, 100], labels=["<20", "20-29", "30-39", "40-49", "50-59", "60+"])
by_group = cleaned.assign(Age_Group=age_bins).groupby(["Age_Group", "Outcome"]).size().reset_index(name="Count")
fig = px.bar(by_group, x="Age_Group", y="Count", color="Outcome", barmode="group", title="Diabetes Distribution by Age Group")
st.plotly_chart(fig, use_container_width=True)

corr = cleaned.corr(numeric_only=True)
heatmap = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r")
heatmap.update_layout(title="Correlation Heatmap")
st.plotly_chart(heatmap, use_container_width=True)
