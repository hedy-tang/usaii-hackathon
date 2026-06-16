import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


def build_weak_labels(df):

    # heuristic confidence signal
    return (
            0.35 * df["certainty"] +
            0.45 * (1 - df["contradiction_severity"]) +
            0.2 * (df["source_type"] / 2)
    )


def train_confidence_model(X):

    y = build_weak_labels(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    return model
