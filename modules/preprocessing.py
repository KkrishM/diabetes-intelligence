from __future__ import annotations

from typing import Dict, Tuple

import numpy as np
import pandas as pd

from utils.helpers import EXPECTED_COLUMNS, MEDICAL_ZERO_COLUMNS


def load_dataset(path: str):
    """Load a CSV file and normalize the headers."""
    try:
        df = pd.read_csv(path)
    except Exception:
        df = pd.read_csv(path, header=None)

    if df.shape[1] == len(EXPECTED_COLUMNS) and not set(df.columns).issubset(set(EXPECTED_COLUMNS)):
        df.columns = EXPECTED_COLUMNS
    else:
        df.columns = [str(col).strip() for col in df.columns]

    if set(df.columns) != set(EXPECTED_COLUMNS):
        df.columns = EXPECTED_COLUMNS

    return df


def validate_dataset(df: pd.DataFrame) -> None:
    missing = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    for col in EXPECTED_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    invalid_outcome = df["Outcome"].isin([0, 1])
    if invalid_outcome.sum() != len(df):
        bad_rows = int((~invalid_outcome).sum())
        raise ValueError(f"Outcome column contains {bad_rows} invalid values. It must be 0 or 1 only.")


def clean_dataset(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """Handle zero-values, missing values, and duplicates in a medically safe manner."""
    cleaned = df.copy()
    report = {
        "before_missing": int(cleaned.isna().sum().sum()),
        "before_duplicates": int(cleaned.duplicated().sum()),
    }

    for col in MEDICAL_ZERO_COLUMNS:
        cleaned[col] = cleaned[col].replace(0, np.nan)

    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    for col in ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "Age", "Pregnancies"]:
        cleaned[col] = cleaned[col].fillna(cleaned[col].median())

    cleaned["DiabetesPedigreeFunction"] = cleaned["DiabetesPedigreeFunction"].fillna(
        cleaned["DiabetesPedigreeFunction"].median()
    )

    cleaned["Outcome"] = cleaned["Outcome"].astype(int)
    report["after_missing"] = int(cleaned.isna().sum().sum())
    report["after_duplicates"] = int(cleaned.duplicated().sum())
    return cleaned, report


def detect_outliers(df: pd.DataFrame) -> Dict[str, int]:
    numeric = [col for col in EXPECTED_COLUMNS if col != "Outcome"]
    summary = {}
    for col in numeric:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        summary[col] = int(((df[col] < lower) | (df[col] > upper)).sum())
    return summary


def prepare_processed_dataset(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, object]]:
    validate_dataset(df)
    cleaned, report = clean_dataset(df)
    outliers = detect_outliers(cleaned)
    processed = cleaned.copy()
    processed["Outcome"] = processed["Outcome"].astype(int)
    summary = {
        "original_shape": df.shape,
        "cleaned_shape": processed.shape,
        "missing_report": report,
        "outlier_summary": outliers,
    }
    return processed, summary
