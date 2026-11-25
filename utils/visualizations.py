from __future__ import annotations

import matplotlib.pyplot as plt


def plot_missing_values(before: int, after: int):
    labels = ["Before cleaning", "After cleaning"]
    values = [before, after]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(labels, values, color=["#ffb703", "#2a9d8f"])
    ax.set_title("Missing Value Counts")
    ax.set_ylabel("Count")
    plt.tight_layout()
    return fig


def plot_outlier_summary(summary: dict):
    labels = list(summary.keys())
    values = list(summary.values())
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values, color="#4cc9f0")
    ax.set_title("Outlier Count by Feature")
    ax.set_ylabel("Outliers")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig
