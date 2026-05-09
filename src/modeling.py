import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler


def build_logistic_regression_pipeline(random_state: int = 42) -> Pipeline:
    """Build a simple baseline classification pipeline."""
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=random_state,
                ),
            ),
        ]
    )


def evaluate_leave_one_out_classifier(X: np.ndarray, y: np.ndarray) -> dict:
    """
    Evaluate a classifier using Leave-One-Out cross-validation.

    This is intended for small-sample exploratory analysis.
    """
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    model = build_logistic_regression_pipeline()
    cv = LeaveOneOut()

    y_pred_encoded = cross_val_predict(
        model,
        X,
        y_encoded,
        cv=cv,
    )

    y_true = label_encoder.inverse_transform(y_encoded)
    y_pred = label_encoder.inverse_transform(y_pred_encoded)

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
        "macro_f1": f1_score(y_true, y_pred, average="macro"),
        "weighted_f1": f1_score(y_true, y_pred, average="weighted"),
        "classification_report": classification_report(
            y_true,
            y_pred,
            zero_division=0,
        ),
        "confusion_matrix": confusion_matrix(
            y_true,
            y_pred,
            labels=label_encoder.classes_,
        ),
        "labels": label_encoder.classes_,
        "y_true": y_true,
        "y_pred": y_pred,
    }

    return metrics


def metrics_to_dataframe(metrics: dict) -> pd.DataFrame:
    """Convert selected metrics into a one-row DataFrame."""
    return pd.DataFrame(
        [
            {
                "accuracy": metrics["accuracy"],
                "balanced_accuracy": metrics["balanced_accuracy"],
                "macro_f1": metrics["macro_f1"],
                "weighted_f1": metrics["weighted_f1"],
            }
        ]
    )
