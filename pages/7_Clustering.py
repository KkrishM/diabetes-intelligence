from __future__ import annotations

import streamlit as st

from modules.clustering import compute_elbow, fit_kmeans
from modules.preprocessing import load_dataset, prepare_processed_dataset
from utils.helpers import ensure_default_dataset

st.set_page_config(page_title="Clustering", layout="wide")

st.title("K-Means Clustering")

try:
    dataset_path = ensure_default_dataset()
    cleaned, _ = prepare_processed_dataset(load_dataset(dataset_path))
except Exception as exc:
    st.error(f"Clustering dataset preparation failed: {exc}")
    st.stop()

max_k = st.slider("Select maximum K for elbow method", 3, 10, 8)
elbow_fig, _ = compute_elbow(cleaned, max_k=max_k)
st.pyplot(elbow_fig, use_container_width=True)

k = st.slider("Choose number of clusters", 2, 6, 3)
cluster_df, summary, silhouette = fit_kmeans(cleaned, k=k)
st.subheader("Cluster summary")
st.dataframe(summary, use_container_width=True)

st.write(f"Silhouette score: {silhouette:.4f}")

st.markdown("### Cluster interpretation")
st.markdown(
    """
    Each cluster represents a group of patients with similar health profiles based on glucose, BMI, age, and insulin.
    These groups are exploratory and should not be treated as medically validated diagnoses.
    """
)
