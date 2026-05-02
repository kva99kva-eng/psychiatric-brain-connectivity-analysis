import nbformat as nbf
from pathlib import Path

notebook_path = Path("notebooks/04_statistical_testing.ipynb")

nb = nbf.v4.new_notebook()

nb["cells"] = [
    nbf.v4.new_markdown_cell("""# Exploratory Statistical Testing of Functional Connectivity Differences

## Goal

This notebook performs exploratory statistical testing of functional connectivity differences between diagnostic groups and healthy controls.

The current sample size is small, so the results are intended to demonstrate the analysis workflow rather than provide clinical or scientific conclusions.
"""),

    nbf.v4.new_code_cell("""from pathlib import Path
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from nilearn import datasets, plotting

PROJECT_ROOT = Path("..").resolve()

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.statistics import (
    vectorize_upper_triangle,
    reconstruct_symmetric_matrix,
    permutation_group_comparison,
)

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CONNECTIVITY_DIR = PROCESSED_DIR / "connectivity"
"""),

    nbf.v4.new_markdown_cell("## Load group connectivity results"),

    nbf.v4.new_code_cell("""results_path = PROCESSED_DIR / "group_connectivity_results.tsv"

results_df = pd.read_csv(results_path, sep="\\t")

results_df
"""),

    nbf.v4.new_code_cell("""successful_subjects = results_df[results_df["status"] == "success"].copy()

successful_subjects["diagnosis"].value_counts()
"""),

    nbf.v4.new_markdown_cell("## Load ROI labels"),

    nbf.v4.new_code_cell("""atlas = datasets.fetch_atlas_harvard_oxford(
    atlas_name="cort-maxprob-thr25-2mm"
)

roi_labels = atlas.labels[1:]

print(f"Number of ROI labels: {len(roi_labels)}")
print(roi_labels[:10])
"""),

    nbf.v4.new_markdown_cell("## Load subject-level connectivity matrices"),

    nbf.v4.new_code_cell("""matrices = {}

for _, row in successful_subjects.iterrows():
    subject_id = row["participant_id"]
    matrix_path = CONNECTIVITY_DIR / f"{subject_id}_connectivity_matrix.npy"
    
    if matrix_path.exists():
        matrices[subject_id] = np.load(matrix_path)
    else:
        print(f"Missing matrix for {subject_id}: {matrix_path}")

print(f"Loaded matrices: {len(matrices)}")
"""),

    nbf.v4.new_markdown_cell("## Vectorize connectivity matrices"),

    nbf.v4.new_code_cell("""vectors = {}
triu_indices = None
matrix_size = None

for subject_id, matrix in matrices.items():
    vector, current_triu_indices = vectorize_upper_triangle(matrix)
    vectors[subject_id] = vector
    
    if triu_indices is None:
        triu_indices = current_triu_indices
        matrix_size = matrix.shape[0]

print(f"Number of edges per subject: {len(next(iter(vectors.values())))}")
print(f"Matrix size: {matrix_size} × {matrix_size}")
"""),

    nbf.v4.new_markdown_cell("## Prepare group arrays"),

    nbf.v4.new_code_cell("""group_vectors = {}

for diagnosis, group_df in successful_subjects.groupby("diagnosis"):
    subject_ids = group_df["participant_id"].tolist()
    available_subject_ids = [subject_id for subject_id in subject_ids if subject_id in vectors]
    
    group_vectors[diagnosis] = np.vstack([
        vectors[subject_id] for subject_id in available_subject_ids
    ])
    
    print(f"{diagnosis}: {group_vectors[diagnosis].shape}")
"""),

    nbf.v4.new_code_cell("""list(group_vectors.keys())
"""),

    nbf.v4.new_markdown_cell("## Permutation testing against healthy controls"),

    nbf.v4.new_code_cell("""control_label = "CONTROL"

if control_label not in group_vectors:
    raise ValueError(f"Control group '{control_label}' not found. Available groups: {list(group_vectors.keys())}")

comparison_results = {}

for diagnosis, patient_vectors in group_vectors.items():
    if diagnosis == control_label:
        continue
    
    print(f"Comparing {diagnosis} vs {control_label}")
    
    results = permutation_group_comparison(
        control_vectors=group_vectors[control_label],
        patient_vectors=patient_vectors,
        roi_labels=roi_labels,
        triu_indices=triu_indices,
        n_permutations=1000,
        alpha=0.05,
        random_state=42,
    )
    
    comparison_results[diagnosis] = results
    
    display(results.head(10))
"""),

    nbf.v4.new_markdown_cell("## Visualize mean difference matrices"),

    nbf.v4.new_code_cell("""for diagnosis in comparison_results.keys():
    mean_patient = np.nanmean(group_vectors[diagnosis], axis=0)
    mean_control = np.nanmean(group_vectors[control_label], axis=0)
    mean_difference_vector = mean_patient - mean_control
    
    difference_matrix = reconstruct_symmetric_matrix(
        vector=mean_difference_vector,
        triu_indices=triu_indices,
        matrix_size=matrix_size,
    )
    
    plotting.plot_matrix(
        difference_matrix,
        figure=(8, 7),
        vmin=-0.5,
        vmax=0.5,
        reorder=False,
        title=f"Mean connectivity difference: {diagnosis} - {control_label}",
    )
    
    plt.show()
"""),

    nbf.v4.new_markdown_cell("## FDR-significant edges"),

    nbf.v4.new_code_cell("""for diagnosis, results in comparison_results.items():
    n_significant = results["significant_fdr"].sum()
    print(f"{diagnosis}: {n_significant} FDR-significant edges")
    
    if n_significant > 0:
        display(results[results["significant_fdr"]].head(20))
"""),

    nbf.v4.new_markdown_cell("## Save statistical results"),

    nbf.v4.new_code_cell("""stats_dir = PROCESSED_DIR / "statistics"
stats_dir.mkdir(parents=True, exist_ok=True)

for diagnosis, results in comparison_results.items():
    output_path = stats_dir / f"permutation_statistics_{diagnosis}_vs_{control_label}.tsv"
    results.to_csv(output_path, sep="\\t", index=False)
    print(f"Saved: {output_path}")
"""),

    nbf.v4.new_markdown_cell("""## Summary

This notebook implemented an exploratory statistical workflow for functional connectivity differences.

Completed steps:

- loaded subject-level connectivity matrices;
- vectorized ROI-to-ROI connectivity matrices;
- compared diagnostic groups against healthy controls;
- performed edge-wise permutation testing;
- applied Benjamini-Hochberg FDR correction;
- saved edge-wise statistical results.

Important limitation:

The current sample size is too small for clinical or scientific conclusions. The purpose of this notebook is to demonstrate a reproducible statistical workflow that can be scaled to larger samples.
""")
]

notebook_path.parent.mkdir(parents=True, exist_ok=True)

with notebook_path.open("w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Created notebook: {notebook_path}")