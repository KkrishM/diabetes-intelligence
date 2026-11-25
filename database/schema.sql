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
