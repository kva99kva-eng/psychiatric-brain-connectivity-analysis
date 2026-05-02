import nbformat as nbf
from pathlib import Path

notebook_path = Path("notebooks/05_ml_classification.ipynb")

nb = nbf.v4.new_notebook()

nb["cells"] = [
    nbf.v4.new_markdown_cell("""# Baseline Machine Learning Classification from Functional Connectivity

## Goal

This notebook builds an exploratory machine learning pipeline using functional connectivity features.

The goal is not to create a clinical diagnostic model, but to demonstrate how subject-level connectomes can be converted into feature vectors and used in a leakage-safe classification workflow.

## Important limitation

The current sample size is very small. Therefore, classification metrics should be interpreted only as a technical validation of the pipeline, not as scientific or clinical evidence.
"""),

    nbf.v4.new_code_cell("""from pathlib import Path
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import ConfusionMatrixDisplay

PROJECT_ROOT = Path("..").resolve()

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.statistics import vectorize_upper_triangle
from src.modeling import evaluate_leave_one_out_classifier, metrics_to_dataframe

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CONNECTIVITY_DIR = PROCESSED_DIR / "connectivity"
"""),

    nbf.v4.new_markdown_cell("## Load subject-level connectivity results"),

    nbf.v4.new_code_cell("""results_path = PROCESSED_DIR / "group_connectivity_results.tsv"

results_df = pd.read_csv(results_path, sep="\\t")

successful_subjects = results_df[results_df["status"] == "success"].copy()

successful_subjects
"""),

    nbf.v4.new_code_cell("""successful_subjects["diagnosis"].value_counts()
"""),

    nbf.v4.new_markdown_cell("## Load and vectorize connectivity matrices"),

    nbf.v4.new_code_cell("""X = []
y_multiclass = []
subject_ids = []

for _, row in successful_subjects.iterrows():
    subject_id = row["participant_id"]
    diagnosis = row["diagnosis"]
    
    matrix_path = CONNECTIVITY_DIR / f"{subject_id}_connectivity_matrix.npy"
    
    if not matrix_path.exists():
        print(f"Missing matrix: {matrix_path}")
        continue
    
    matrix = np.load(matrix_path)
    vector, _ = vectorize_upper_triangle(matrix)
    
    X.append(vector)
    y_multiclass.append(diagnosis)
    subject_ids.append(subject_id)

X = np.vstack(X)
y_multiclass = np.array(y_multiclass)

print(f"Feature matrix shape: {X.shape}")
print(f"Labels shape: {y_multiclass.shape}")
"""),

    nbf.v4.new_markdown_cell("""## Multiclass classification

This task attempts to classify diagnostic groups directly.

Because the sample size is very small, this section is included only to demonstrate the classification workflow.
"""),

    nbf.v4.new_code_cell("""multiclass_metrics = evaluate_leave_one_out_classifier(X, y_multiclass)

metrics_to_dataframe(multiclass_metrics)
"""),

    nbf.v4.new_code_cell("""print(multiclass_metrics["classification_report"])
"""),

    nbf.v4.new_code_cell("""disp = ConfusionMatrixDisplay(
    confusion_matrix=multiclass_metrics["confusion_matrix"],
    display_labels=multiclass_metrics["labels"],
)

disp.plot(xticks_rotation=45)
plt.title("Multiclass classification confusion matrix")
plt.tight_layout()
plt.show()
"""),

    nbf.v4.new_markdown_cell("""## Binary classification: psychiatric group vs healthy controls

This task collapses all psychiatric diagnoses into a single group and compares them against healthy controls.
"""),

    nbf.v4.new_code_cell("""y_binary = np.where(y_multiclass == "CONTROL", "CONTROL", "PSYCHIATRIC")

pd.Series(y_binary).value_counts()
"""),

    nbf.v4.new_code_cell("""binary_metrics = evaluate_leave_one_out_classifier(X, y_binary)

metrics_to_dataframe(binary_metrics)
"""),

    nbf.v4.new_code_cell("""print(binary_metrics["classification_report"])
"""),

    nbf.v4.new_code_cell("""disp = ConfusionMatrixDisplay(
    confusion_matrix=binary_metrics["confusion_matrix"],
    display_labels=binary_metrics["labels"],
)

disp.plot()
plt.title("Binary classification confusion matrix")
plt.tight_layout()
plt.show()
"""),

    nbf.v4.new_markdown_cell("""## Save ML results"""),

    nbf.v4.new_code_cell("""ml_dir = PROCESSED_DIR / "ml"
ml_dir.mkdir(parents=True, exist_ok=True)

multiclass_metrics_path = ml_dir / "multiclass_metrics.tsv"
binary_metrics_path = ml_dir / "binary_metrics.tsv"
predictions_path = ml_dir / "ml_predictions.tsv"

metrics_to_dataframe(multiclass_metrics).to_csv(multiclass_metrics_path, sep="\\t", index=False)
metrics_to_dataframe(binary_metrics).to_csv(binary_metrics_path, sep="\\t", index=False)

predictions_df = pd.DataFrame({
    "participant_id": subject_ids,
    "true_multiclass": multiclass_metrics["y_true"],
    "predicted_multiclass": multiclass_metrics["y_pred"],
    "true_binary": binary_metrics["y_true"],
    "predicted_binary": binary_metrics["y_pred"],
})

predictions_df.to_csv(predictions_path, sep="\\t", index=False)

print(f"Saved: {multiclass_metrics_path}")
print(f"Saved: {binary_metrics_path}")
print(f"Saved: {predictions_path}")
"""),

    nbf.v4.new_markdown_cell("""## Summary

This notebook implemented a baseline machine learning workflow for functional connectivity features.

Completed steps:

- loaded subject-level connectivity matrices;
- vectorized upper-triangle connectivity edges;
- built leakage-safe classification pipelines using scaling inside cross-validation;
- evaluated multiclass diagnostic classification;
- evaluated binary psychiatric-vs-control classification;
- saved metrics and prediction tables.

Important limitation:

The current sample size is too small for scientific interpretation. The purpose of this notebook is to demonstrate a reproducible ML workflow that can be scaled to larger samples.
""")
]

notebook_path.parent.mkdir(parents=True, exist_ok=True)

with notebook_path.open("w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Created notebook: {notebook_path}")