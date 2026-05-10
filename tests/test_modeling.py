import numpy as np
from sklearn.pipeline import Pipeline

from src.modeling import (
    build_logistic_regression_pipeline,
    evaluate_leave_one_out_classifier,
    metrics_to_dataframe,
)


def test_build_logistic_regression_pipeline_returns_pipeline():
    pipeline = build_logistic_regression_pipeline()

    assert isinstance(pipeline, Pipeline)
    assert "scaler" in pipeline.named_steps
    assert "classifier" in pipeline.named_steps


def test_evaluate_leave_one_out_classifier_returns_expected_keys():
    X = np.array(
        [
            [-3.0, 0.0],
            [-2.0, 0.0],
            [-1.0, 0.0],
            [1.0, 0.0],
            [2.0, 0.0],
            [3.0, 0.0],
        ]
    )
    y = np.array(
        [
            "control",
            "control",
            "control",
            "patient",
            "patient",
            "patient",
        ]
    )

    metrics = evaluate_leave_one_out_classifier(X, y)

    expected_keys = {
        "accuracy",
        "balanced_accuracy",
        "macro_f1",
        "weighted_f1",
        "classification_report",
        "confusion_matrix",
        "labels",
        "y_true",
        "y_pred",
    }

    assert expected_keys.issubset(metrics.keys())
    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert 0.0 <= metrics["balanced_accuracy"] <= 1.0
    assert metrics["confusion_matrix"].shape == (2, 2)


def test_metrics_to_dataframe_returns_one_row_dataframe():
    metrics = {
        "accuracy": 0.75,
        "balanced_accuracy": 0.70,
        "macro_f1": 0.72,
        "weighted_f1": 0.74,
    }

    df = metrics_to_dataframe(metrics)

    assert df.shape == (1, 4)
    assert list(df.columns) == [
        "accuracy",
        "balanced_accuracy",
        "macro_f1",
        "weighted_f1",
    ]
