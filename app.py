from __future__ import annotations

import streamlit as st

from modules.preprocessing import load_dataset, prepare_processed_dataset
from modules.etl import run_etl
from utils.helpers import ensure_default_dataset, get_db_path

st.set_page_config(page_title="Diabetes Intelligence", page_icon="🩺", layout="wide")

st.title("Diabetes Intelligence – Healthcare Analytics Platform")
st.caption("Academic Data Mining and Data Warehousing project")

st.markdown(
    """
    This application demonstrates ETL, data warehousing, OLAP analysis, exploratory analysis,
    classification, clustering, and patient risk prediction using the Pima Indians Diabetes dataset.
    """
)

with st.sidebar:
    st.header("Project Navigation")
    st.page_link("app.py", label="Home")


def home_setup():
    dataset_path = ensure_default_dataset()
    try:
        df = load_dataset(dataset_path)
        cleaned, _ = prepare_processed_dataset(df)
        db_path = get_db_path()
        run_etl(dataset_path, db_path)
        st.success(f"Loaded dataset with {len(cleaned)} cleaned records. Warehouse ready at {db_path.name}.")
    except Exception as exc:
        st.error(f"Initialization failed: {exc}")

home_setup()

st.subheader("System overview")
col1, col2, col3 = st.columns(3)
col1.metric("Dataset", "Pima Indians Diabetes")
col2.metric("Warehouse", "SQLite")
col3.metric("UI", "Streamlit")

st.markdown("### Main modules")
for label in [
    "Dashboard Overview",
    "Data Preprocessing and ETL",
    "Data Warehouse",
    "OLAP Analysis",
    "Exploratory Analysis",
    "Classification",
    "Clustering",
    "Prediction",
]:
    st.markdown(f"- {label}")
