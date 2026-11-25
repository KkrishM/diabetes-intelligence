from __future__ import annotations

import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from modules.classification import run_classification
from modules.preprocessing import load_dataset, prepare_processed_dataset
from utils.helpers import ensure_default_dataset

st.set_page_config(page_title="Classification", layout="wide")

st.title("Data Mining and Classification")

try:
    dataset_path = ensure_default_dataset()
    raw = load_dataset(dataset_path)
    cleaned, _ = prepare_processed_dataset(raw)
    result = run_classification(cleaned)
except Exception as exc:
    st.error(f"Classification failed: {exc}")
    st.stop()

st.subheader("Model comparison")
st.dataframe(result["table"], use_container_width=True)

st.subheader("Confusion matrices")
for label, model_result in [("Logistic Regression", result["logistic"]), ("Random Forest", result["random_forest"])]:
    fig, ax = plt.subplots(figsize=(4, 4))
    sns.heatmap(model_result["confusion_matrix"], annot=True, fmt="d", cmap="Blues", xticklabels=["Non-Diabetic", "Diabetic"], yticklabels=["Non-Diabetic", "Diabetic"], ax=ax)
    ax.set_title(label)
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("Actual Label")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

st.subheader("ROC curve")
st.pyplot(result["roc_figure"], use_container_width=True)

st.markdown("### Interpretation")
st.markdown(
    """
    The comparison table reports the actual evaluation metrics for both models. A more accurate interpretation depends
    on precision, recall, and F1-score rather than accuracy alone. The model with the better balance of recall and
    precision should be preferred when evaluated on the held-out test data.
    """
)
