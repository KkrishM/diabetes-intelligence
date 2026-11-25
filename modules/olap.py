from __future__ import annotations

from pathlib import Path

from database.warehouse import quick_query


def olap_queries(db_path: str | Path):
    db_path = Path(db_path)
    queries = {
        "Roll-up": """
            SELECT pd.Age_Group,
                   COUNT(*) AS Total_Patients,
                   SUM(CASE WHEN od.Diabetes_Outcome = 1 THEN 1 ELSE 0 END) AS Diabetic_Cases
            FROM Diabetes_Fact f
            JOIN Patient_Dimension pd ON pd.Patient_ID = f.Patient_ID
            JOIN Outcome_Dimension od ON od.Outcome_ID = f.Outcome_ID
            GROUP BY pd.Age_Group
            ORDER BY pd.Age_Group
        """,
        "Drill-down": """
            SELECT pd.Age_Group,
                   pd.Age,
                   hd.BMI_Category,
                   hd.Glucose_Category,
                   COUNT(*) AS Cases
            FROM Diabetes_Fact f
            JOIN Patient_Dimension pd ON pd.Patient_ID = f.Patient_ID
            JOIN Health_Dimension hd ON hd.Health_ID = f.Health_ID
            JOIN Outcome_Dimension od ON od.Outcome_ID = f.Outcome_ID
            WHERE od.Diabetes_Outcome = 1
            GROUP BY pd.Age_Group, pd.Age, hd.BMI_Category, hd.Glucose_Category
            ORDER BY pd.Age_Group, pd.Age
            LIMIT 20
        """,
        "Slice": """
            SELECT f.Fact_ID, pd.Patient_ID, pd.Age_Group, od.Diabetes_Outcome, f.Glucose, f.BMI
            FROM Diabetes_Fact f
            JOIN Patient_Dimension pd ON pd.Patient_ID = f.Patient_ID
            JOIN Outcome_Dimension od ON od.Outcome_ID = f.Outcome_ID
            WHERE od.Diabetes_Outcome = 1
            ORDER BY f.Fact_ID
            LIMIT 20
        """,
        "Dice": """
            SELECT pd.Patient_ID, pd.Age, pd.Age_Group, f.Glucose, f.BMI, od.Diabetes_Outcome
            FROM Diabetes_Fact f
            JOIN Patient_Dimension pd ON pd.Patient_ID = f.Patient_ID
            JOIN Health_Dimension hd ON hd.Health_ID = f.Health_ID
            JOIN Outcome_Dimension od ON od.Outcome_ID = f.Outcome_ID
            WHERE pd.Age BETWEEN 30 AND 50
              AND f.BMI > 25
              AND f.Glucose > 120
              AND od.Diabetes_Outcome = 1
            ORDER BY pd.Age
        """,
    }
    result = {}
    for label, sql in queries.items():
        result[label] = quick_query(db_path, sql)
    return result
