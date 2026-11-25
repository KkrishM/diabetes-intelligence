from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

CLUSTER_FEATURES = ["Glucose", "BMI", "Age", "Insulin"]


def compute_elbow(df: pd.DataFrame, max_k: int = 8):
    X = df[CLUSTER_FEATURES].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    inertias = []
    for k in range(1, max_k + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inertias.append(km.inertia_)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(range(1, max_k + 1), inertias, marker="o")
    ax.set_title("Elbow Method for K Selection")
    ax.set_xlabel("Number of clusters (k)")
    ax.set_ylabel("Inertia")
    fig.tight_layout()
    return fig, inertias


def fit_kmeans(df: pd.DataFrame, k: int = 3):
    X = df[CLUSTER_FEATURES].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(X_scaled)
    cluster_df = df.copy()
    cluster_df["Cluster"] = labels
    cluster_summary = cluster_df.groupby("Cluster")[CLUSTER_FEATURES + ["Outcome"]].mean().round(2)
    silhouette = silhouette_score(X_scaled, labels)
    return cluster_df, cluster_summary, silhouette
