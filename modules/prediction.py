from __future__ import annotations

import pandas as pd
import joblib

from modules.classification import run_classification
from modules.preprocessing import load_dataset, prepare_processed_dataset
from utils.helpers import ensure_default_dataset, get_model_path

FEATURE_COLUMNS = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
]


def load_models():
    logistic_path = get_model_path("logistic_regression.pkl")
    forest_path = get_model_path("random_forest.pkl")
    if not logistic_path.exists() or not forest_path.exists():
        df = load_dataset(ensure_default_dataset())
        cleaned, _ = prepare_processed_dataset(df)
        run_classification(cleaned)
    logistic = joblib.load(logistic_path)
    forest = joblib.load(forest_path)
    return {"logistic_regression": logistic, "random_forest": forest}


def predict_patient(data: dict):
    row = {feature: float(data.get(feature, 0)) for feature in FEATURE_COLUMNS}
    frame = pd.DataFrame([row])
    models = load_models()

    logistic_pred = models["logistic_regression"].predict(frame)[0]
    forest_pred = models["random_forest"].predict(frame)[0]

    logistic_prob = models["logistic_regression"].predict_proba(frame)[0, 1]
    forest_prob = models["random_forest"].predict_proba(frame)[0, 1]

    return {
        "logistic_regression": {
            "prediction": int(logistic_pred),
            "probability": float(logistic_prob),
        },
        "random_forest": {
            "prediction": int(forest_pred),
            "probability": float(forest_prob),
        },
    }
