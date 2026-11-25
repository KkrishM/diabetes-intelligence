# Diabetes Intelligence – Healthcare Analytics Platform

This project is a complete academic data mining and data warehousing application for the Pima Indians Diabetes dataset. It demonstrates ETL, data preprocessing, star-schema warehouse design, OLAP operations, exploratory analysis, classification, clustering, and predictive analytics using Python and Streamlit.

## Problem statement
Diabetes is a major public health issue. This project applies data mining and data warehousing principles to analyse patient health indicators and classify risk patterns using a real clinical dataset. The application is designed for demonstration and academic learning rather than medical diagnosis.

## Objectives
- Load and validate the Pima Indians Diabetes dataset
- Process missing and invalid values using medically careful rules
- Build an SQLite-based star schema data warehouse
- Execute real OLAP operations using SQL queries
- Explore patterns with statistical and visual analysis
- Train and compare Logistic Regression and Random Forest models
- Use K-Means clustering for unsupervised pattern discovery
- Deliver an interactive prediction interface

## Technology stack
- Python
- Streamlit
- pandas, NumPy
- scikit-learn
- SQLite
- Plotly, Matplotlib, Seaborn
- joblib

## Dataset description
The Pima Indians Diabetes dataset includes the following attributes:
- Pregnancies
- Glucose
- BloodPressure
- SkinThickness
- Insulin
- BMI
- DiabetesPedigreeFunction
- Age
- Outcome (0 = Non-Diabetic, 1 = Diabetic)

The dataset is downloaded into `data/diabetes.csv` automatically if missing.

## System architecture
The project is modular and separated by responsibility:
- `app.py` – Streamlit application entry point
- `database/` – SQLite schema and warehouse logic
- `modules/` – ETL, preprocessing, OLAP, EDA, classification, clustering, prediction
- `pages/` – Multi-page dashboard sections
- `utils/` – shared helper functions and visual wrappers
- `models/` – trained ML model files

## ETL workflow
1. Load CSV dataset
2. Validate required columns and types
3. Replace medically invalid zero values with missing values
4. Remove duplicate rows
5. Impute missing values using medians
6. Detect outliers
7. Build clean dataset for modelling and warehousing
8. Store processed data in SQLite warehouse tables

## Data warehouse schema
The star schema includes:
- `Diabetes_Fact`
- `Patient_Dimension`
- `Health_Dimension`
- `Outcome_Dimension`

These tables are connected through Primary Key and Foreign Key constraints.

## OLAP operations
The application demonstrates actual SQL queries for:
- Roll-up by age group
- Drill-down by age and health dimension
- Slice by diabetes outcome
- Dice by BMI, age, glucose, and outcome filters

## Data mining algorithms
The project implements:
- Logistic Regression
- Random Forest Classifier
- K-Means Clustering

## Model evaluation
Model performance is evaluated using:
- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix
- ROC curve
- AUC

## Installation
```bash
pip install -r requirements.txt
```

## Run the app
```bash
streamlit run app.py
```

## Future scope
- Add automated model retraining from uploaded files
- Add patient history tracking
- Introduce advanced feature engineering
- Export reports to PDF or Excel
- Connect to a larger hospital data warehouse model
