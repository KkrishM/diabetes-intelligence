from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from utils.helpers import age_group, bmi_category, blood_pressure_category, glucose_category, pregnancy_category

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS Patient_Dimension (
    Patient_ID INTEGER PRIMARY KEY,
    Age INTEGER,
    Age_Group TEXT,
    Pregnancy_Category TEXT
);

CREATE TABLE IF NOT EXISTS Health_Dimension (
    Health_ID INTEGER PRIMARY KEY,
    BMI_Category TEXT,
    Glucose_Category TEXT,
    BloodPressure_Category TEXT
);

CREATE TABLE IF NOT EXISTS Outcome_Dimension (
    Outcome_ID INTEGER PRIMARY KEY,
    Diabetes_Outcome INTEGER,
    Risk_Category TEXT
);

CREATE TABLE IF NOT EXISTS Diabetes_Fact (
    Fact_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Patient_ID INTEGER,
    Health_ID INTEGER,
    Outcome_ID INTEGER,
    Glucose REAL,
    BloodPressure REAL,
    SkinThickness REAL,
    Insulin REAL,
    BMI REAL,
    DiabetesPedigreeFunction REAL,
    Age INTEGER,
    Pregnancies INTEGER,
    FOREIGN KEY (Patient_ID) REFERENCES Patient_Dimension(Patient_ID),
    FOREIGN KEY (Health_ID) REFERENCES Health_Dimension(Health_ID),
    FOREIGN KEY (Outcome_ID) REFERENCES Outcome_Dimension(Outcome_ID)
);
"""


def get_connection(db_path: str | Path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_star_schema(db_path: str | Path):
    db_path = Path(db_path)
    db_path.parent.mkdir(exist_ok=True, parents=True)
    conn = get_connection(db_path)
    try:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()


def build_star_schema(db_path: str | Path, df: pd.DataFrame):
    create_star_schema(db_path)
    conn = get_connection(db_path)
    try:
        conn.execute("DELETE FROM Diabetes_Fact")
        conn.execute("DELETE FROM Patient_Dimension")
        conn.execute("DELETE FROM Health_Dimension")
        conn.execute("DELETE FROM Outcome_Dimension")

        conn.executemany(
            "INSERT INTO Outcome_Dimension (Outcome_ID, Diabetes_Outcome, Risk_Category) VALUES (?, ?, ?)",
            [(1, 0, "Low Risk"), (2, 1, "High Risk")],
        )

        patient_rows = []
        health_rows = []
        health_map = {}
        fact_rows = []

        for index, row in df.reset_index(drop=True).iterrows():
            patient_id = int(index + 1)
            patient_rows.append(
                (
                    patient_id,
                    int(row["Age"]),
                    age_group(int(row["Age"])),
                    pregnancy_category(float(row["Pregnancies"])),
                )
            )

            health_key = (
                bmi_category(float(row["BMI"])),
                glucose_category(float(row["Glucose"])),
                blood_pressure_category(float(row["BloodPressure"])),
            )
            if health_key not in health_map:
                health_id = len(health_map) + 1
                health_map[health_key] = health_id
                health_rows.append((health_id, health_key[0], health_key[1], health_key[2]))
            else:
                health_id = health_map[health_key]

            outcome_id = 1 if int(row["Outcome"]) == 0 else 2
            fact_rows.append(
                (
                    patient_id,
                    health_id,
                    outcome_id,
                    float(row["Glucose"]),
                    float(row["BloodPressure"]),
                    float(row["SkinThickness"]),
                    float(row["Insulin"]),
                    float(row["BMI"]),
                    float(row["DiabetesPedigreeFunction"]),
                    int(row["Age"]),
                    int(row["Pregnancies"]),
                )
            )

        conn.executemany(
            "INSERT INTO Patient_Dimension (Patient_ID, Age, Age_Group, Pregnancy_Category) VALUES (?, ?, ?, ?)",
            patient_rows,
        )
        conn.executemany(
            "INSERT INTO Health_Dimension (Health_ID, BMI_Category, Glucose_Category, BloodPressure_Category) VALUES (?, ?, ?, ?)",
            health_rows,
        )
        conn.executemany(
            "INSERT INTO Diabetes_Fact (Patient_ID, Health_ID, Outcome_ID, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, Pregnancies) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            fact_rows,
        )

        conn.commit()
        return True
    finally:
        conn.close()


def quick_query(db_path: str | Path, sql: str):
    conn = get_connection(db_path)
    try:
        return pd.read_sql_query(sql, conn)
    finally:
        conn.close()


def execute_sql(db_path: str | Path, sql: str) -> pd.DataFrame:
    """Run a SQL statement and return either its rows or an execution summary."""
    conn = get_connection(db_path)
    try:
        cursor = conn.execute(sql)
        if cursor.description is not None:
            return pd.DataFrame(cursor.fetchall(), columns=[column[0] for column in cursor.description])
        conn.commit()
        return pd.DataFrame(
            [{"Status": "Executed successfully", "Rows affected": cursor.rowcount}]
        )
    except sqlite3.Error:
        conn.rollback()
        raise
    finally:
        conn.close()
