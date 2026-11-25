from __future__ import annotations

import streamlit as st

from modules.olap import olap_queries
from modules.etl import run_etl
from utils.helpers import ensure_default_dataset, get_db_path

st.set_page_config(page_title="OLAP", layout="wide")

st.title("OLAP Operations")

try:
    db_path = get_db_path()
    run_etl(ensure_default_dataset(), db_path)
    result_map = olap_queries(db_path)
except Exception as exc:
    st.error(f"OLAP query execution failed: {exc}")
    st.stop()

operations = [
    ("Roll-up", "Aggregate cases by age groups instead of individual ages."),
    ("Drill-down", "Explore high-risk cases by age and health category."),
    ("Slice", "Filter by a particular diabetes outcome."),
    ("Dice", "Filter by multiple conditions such as age, BMI, glucose, and outcome."),
]

for label, description in operations:
    st.subheader(label)
    st.caption(description)
    df = result_map[label]
    st.dataframe(df.head(20), use_container_width=True)
    try:
        table_text = df.to_markdown(index=False)
    except Exception:
        table_text = df.to_string(index=False)
    st.code(table_text, language="text")
    st.markdown("---")
