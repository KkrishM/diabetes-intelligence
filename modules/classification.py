from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib

from utils.helpers import get_model_path

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


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

    metrics = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, zero_division=0),
        "Recall": recall_score(y_test, y_pred, zero_division=0),
        "F1": f1_score(y_test, y_pred, zero_division=0),
    }
    cm = confusion_matrix(y_test, y_pred)
    results = {"predictions": y_pred, "metrics": metrics, "confusion_matrix": cm}
    if y_prob is not None:
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        results["roc_curve"] = (fpr, tpr)
        results["auc"] = roc_auc_score(y_test, y_prob)
    return results


def run_classification(df: pd.DataFrame):
    X = df[FEATURE_COLUMNS]
    y = df["Outcome"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42,
    )

    logistic_model = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000, random_state=42)),
    ])
    forest_model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")

    logistic_model.fit(X_train, y_train)
    forest_model.fit(X_train, y_train)

    logistic_results = evaluate_model(logistic_model, X_test, y_test)
    forest_results = evaluate_model(forest_model, X_test, y_test)

    model_table = pd.DataFrame(
        {
            "Model": ["Logistic Regression", "Random Forest"],
            "Accuracy": [
                logistic_results["metrics"]["Accuracy"],
                forest_results["metrics"]["Accuracy"],
            ],
            "Precision": [
                logistic_results["metrics"]["Precision"],
                forest_results["metrics"]["Precision"],
            ],
            "Recall": [
                logistic_results["metrics"]["Recall"],
                forest_results["metrics"]["Recall"],
            ],
            "F1-Score": [
                logistic_results["metrics"]["F1"],
                forest_results["metrics"]["F1"],
            ],
        }
    ).round(4)

    joblib.dump(logistic_model, get_model_path("logistic_regression.pkl"))
    joblib.dump(forest_model, get_model_path("random_forest.pkl"))

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(logistic_results["roc_curve"][0], logistic_results["roc_curve"][1], label=f"Logistic Regression (AUC={logistic_results['auc']:.3f})")
    ax.plot(forest_results["roc_curve"][0], forest_results["roc_curve"][1], label=f"Random Forest (AUC={forest_results['auc']:.3f})")
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve Comparison")
    ax.legend()
    fig.tight_layout()

    return {
        "logistic": logistic_results,
        "random_forest": forest_results,
        "table": model_table,
        "roc_figure": fig,
    }
