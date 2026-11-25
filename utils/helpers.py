from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlopen

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "database"
MODELS_DIR = BASE_DIR / "models"
DEFAULT_DATASET_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
EXPECTED_COLUMNS = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
    "Outcome",
]
MEDICAL_ZERO_COLUMNS = [
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
]


def ensure_project_folders() -> None:
    DATA_DIR.mkdir(exist_ok=True, parents=True)
    DB_DIR.mkdir(exist_ok=True, parents=True)
    MODELS_DIR.mkdir(exist_ok=True, parents=True)


def ensure_default_dataset() -> Path:
    ensure_project_folders()
    path = DATA_DIR / "diabetes.csv"
    if path.exists():
        return path
    with urlopen(DEFAULT_DATASET_URL, timeout=30) as response:
        content = response.read()
    path.write_bytes(content)
    return path


def get_db_path() -> Path:
    ensure_project_folders()
    return DB_DIR / "warehouse.db"


def get_model_path(name: str) -> Path:
    ensure_project_folders()
    return MODELS_DIR / name


def age_group(age: int) -> str:
    if age < 18:
        return "Under 18"
    if age < 30:
        return "18-29"
    if age < 40:
        return "30-39"
    if age < 50:
        return "40-49"
    if age < 60:
        return "50-59"
    return "60+"


def pregnancy_category(pregnancies: float) -> str:
    if pregnancies == 0:
        return "None"
    if pregnancies <= 2:
        return "Low"
    if pregnancies <= 5:
        return "Moderate"
    return "High"


def bmi_category(bmi: float) -> str:
    if pd.isna(bmi):
        return "Unknown"
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def glucose_category(glucose: float) -> str:
    if pd.isna(glucose):
        return "Unknown"
    if glucose < 100:
        return "Normal"
    if glucose < 126:
        return "Prediabetes"
    return "High"


def blood_pressure_category(bp: float) -> str:
    if pd.isna(bp):
        return "Unknown"
    if bp < 80:
        return "Low"
    if bp < 120:
        return "Normal"
    if bp < 140:
        return "Elevated"
    return "High"


def outcome_category(outcome: int) -> str:
    if outcome == 1:
        return "Diabetic"
    return "Non-Diabetic"


def interpret_risk(outcome: int) -> str:
    return "High Risk" if outcome == 1 else "Low Risk"


def load_json(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)
