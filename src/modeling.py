import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import LeaveOneOut
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler


def build_logistic_regression_pipeline(random_state: int = 42) -> Pipeline:
    """
    Build a simple baseline classification pipeline.

    StandardScaler is fitted inside cross-validation to avoid data leakage.
    """
    return Pipeline([
        ("scaler", StandardScaler()),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=random_state,
            ),
        ),
    ])


def evaluate_leave_one_out_classifier(
    X: np.ndarray,
    y: np.ndarray,
    random_state: int = 42,
) -> dict:
    """
    Evaluate a classifier using Leave-One-Out cross-validation.

    Folds where the training set contains only one class are skipped. This can
    happen in extremely small datasets, for example when one class has only
    one subject.
    """
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)

    if X.ndim != 2:
        raise ValueError("X must be a two-dimensional feature matrix.")

    if len(y) != X.shape[0]:
        raise ValueError("X and y must contain the same number of samples.")

    if len(np.unique(y)) < 2:
        raise ValueError("At least two classes are required for classification.")

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    model = build_logistic_regression_pipeline(random_state=random_state)
    cv = LeaveOneOut()

    y_pred_encoded = np.full(shape=len(y_encoded), fill_value=-1, dtype=int)
    skipped_folds = 0

    for train_index, test_index in cv.split(X):
        y_train = y_encoded[train_index]

        if len(np.unique(y_train)) < 2:
            skipped_folds += 1
            continue

        fold_model = clone(model)
        fold_model.fit(X[train_index], y_train)

        y_pred_encoded[test_index] = fold_model.predict(X[test_index])

    valid_mask = y_pred_encoded != -1

    if valid_mask.sum() == 0:
        raise ValueError(
            "No valid cross-validation folds were available. "
            "Increase the number of subjects per class."
        )

    y_true = label_encoder.inverse_transform(y_encoded[valid_mask])
    y_pred = label_encoder.inverse_transform(y_pred_encoded[valid_mask])

    labels = label_encoder.classes_

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
        "macro_f1": f1_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0,
        ),
        "weighted_f1": f1_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0,
        ),
        "classification_report": classification_report(
            y_true,
            y_pred,
            labels=labels,
            target_names=labels,
            zero_division=0,
        ),
        "confusion_matrix": confusion_matrix(
            y_true,
            y_pred,
            labels=labels,
        ),
        "labels": labels,
        "y_true": y_true,
        "y_pred": y_pred,
        "n_samples": len(y),
        "n_evaluated_samples": int(valid_mask.sum()),
        "skipped_folds": skipped_folds,
        "evaluated_indices": np.where(valid_mask)[0],
    }

    return metrics


def metrics_to_dataframe(metrics: dict) -> pd.DataFrame:
    """Convert selected metrics into a one-row DataFrame."""
    return pd.DataFrame([{
        "accuracy": metrics["accuracy"],
        "balanced_accuracy": metrics["balanced_accuracy"],
        "macro_f1": metrics["macro_f1"],
        "weighted_f1": metrics["weighted_f1"],
        "n_samples": metrics.get("n_samples"),
        "n_evaluated_samples": metrics.get("n_evaluated_samples"),
        "skipped_folds": metrics.get("skipped_folds"),
    }])
