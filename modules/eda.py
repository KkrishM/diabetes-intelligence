from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns


def feature_distribution_plots(df: pd.DataFrame):
    plots = {}
    plots["age_distribution"] = px.histogram(df, x="Age", nbins=30, title="Age Distribution")
    plots["glucose_distribution"] = px.histogram(df, x="Glucose", nbins=30, title="Glucose Distribution")
    plots["bmi_distribution"] = px.histogram(df, x="BMI", nbins=30, title="BMI Distribution")
    plots["outcome_pie"] = px.pie(df, names="Outcome", title="Diabetes Distribution", hole=0.45)
    plots["outcome_by_age"] = px.bar(
        df.groupby(["Age", "Outcome"]).size().reset_index(name="Count"),
        x="Age",
        y="Count",
        color="Outcome",
        barmode="group",
        title="Diabetes Cases by Age",
    )
    return plots


def correlation_heatmap(df: pd.DataFrame):
    corr = df.corr(numeric_only=True)
    fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r")
    fig.update_layout(title="Correlation Heatmap")
    return fig


def outcome_scatter_plots(df: pd.DataFrame):
    plots = {}
    for feature in ["Glucose", "BMI", "Age", "Pregnancies"]:
        plots[f"{feature}_vs_outcome"] = px.box(
            df,
            x="Outcome",
            y=feature,
            color="Outcome",
            title=f"{feature} vs Diabetes Outcome",
            category_orders={"Outcome": [0, 1]},
        )
    return plots


def distribution_summary(df: pd.DataFrame):
    return df.describe().round(2)


def plot_pairwise_relationships(df: pd.DataFrame):
    numeric = df.select_dtypes(include="number")
    g = sns.pairplot(numeric[["Glucose", "BMI", "Age", "Pregnancies", "Outcome"]], hue="Outcome", diag_kind="hist", height=1.8)
    plt.tight_layout()
    return g
