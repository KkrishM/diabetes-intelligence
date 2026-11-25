from __future__ import annotations

import streamlit as st

from database.warehouse import execute_sql, quick_query
from modules.preprocessing import load_dataset, prepare_processed_dataset
from modules.etl import run_etl
from utils.helpers import ensure_default_dataset, get_db_path

st.set_page_config(page_title="Warehouse", layout="wide")

st.title("Data Warehouse Design")
st.markdown("A star schema was implemented using SQLite to organize clinical facts and reference dimensions.")

with open("database/schema.sql", "r", encoding="utf-8") as file:
    schema_sql = file.read()

st.code(schema_sql, language="sql")

st.subheader("Purpose of each table")
with st.expander("Diabetes_Fact"):
    st.write("The fact table stores numerical health indicators and links each patient record to the relevant dimension tables.")
with st.expander("Patient_Dimension"):
    st.write("This dimension groups patient-level information such as age and pregnancy category.")
with st.expander("Health_Dimension"):
    st.write("This dimension stores health-state categories like BMI, blood pressure and glucose bands.")
with st.expander("Outcome_Dimension"):
    st.write("This dimension captures diabetic outcome and risk category.")

st.subheader("Database checks")
try:
    df = load_dataset(ensure_default_dataset())
    cleaned, _ = prepare_processed_dataset(df)
    db_path = get_db_path()
    run_etl(ensure_default_dataset(), db_path)
    tables = quick_query(db_path, "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    st.dataframe(tables, use_container_width=True)
except Exception as exc:
    st.error(f"Warehouse setup failed: {exc}")

st.subheader("Schema relationship")
st.markdown(
    """
    Diabetes_Fact -> Patient_Dimension on Patient_ID
    Diabetes_Fact -> Health_Dimension on Health_ID
    Diabetes_Fact -> Outcome_Dimension on Outcome_ID
    """
)

st.subheader("Academic SQL demonstration")
try:
    db_path = get_db_path()
    run_etl(ensure_default_dataset(), db_path)
    sql_examples = {
        "Create table": "CREATE TABLE IF NOT EXISTS Sample_Outcome (Outcome_ID INTEGER PRIMARY KEY, Diabetes_Outcome INTEGER);",
        "Insert data": "INSERT OR IGNORE INTO Sample_Outcome (Outcome_ID, Diabetes_Outcome) VALUES (1, 0), (2, 1);",
        "Select patients": "SELECT * FROM Outcome_Dimension LIMIT 5;",
        "Where filter": "SELECT * FROM Outcome_Dimension WHERE Diabetes_Outcome = 1;",
        "Group by": "SELECT Age_Group, COUNT(*) AS Patient_Count FROM Patient_Dimension GROUP BY Age_Group ORDER BY Patient_Count DESC;",
        "Order by": "SELECT * FROM Patient_Dimension ORDER BY Age DESC LIMIT 5;",
        "Join": "SELECT f.Patient_ID, pd.Age_Group, od.Diabetes_Outcome FROM Diabetes_Fact f JOIN Patient_Dimension pd ON pd.Patient_ID = f.Patient_ID JOIN Outcome_Dimension od ON od.Outcome_ID = f.Outcome_ID LIMIT 10;",
        "Aggregate": "SELECT COUNT(*) AS Diabetic_Record_Count FROM Diabetes_Fact WHERE Outcome_ID = 2;",
        "Subquery": "SELECT * FROM Patient_Dimension WHERE Age > (SELECT AVG(Age) FROM Patient_Dimension);",
    }
    for label, sql in sql_examples.items():
        st.markdown(f"**{label}**")
        st.code(sql, language="sql")
        try:
            result = execute_sql(db_path, sql)
            st.dataframe(result.head(10), use_container_width=True)
        except Exception as exc:
            st.caption(f"Execution error: {exc}")
        st.markdown("---")
except Exception as exc:
    st.error(f"SQL demonstration setup failed: {exc}")
