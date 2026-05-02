# Transdiagnostic Functional Connectivity Analysis in Psychiatric Disorders

This project analyzes resting-state fMRI functional connectivity patterns across psychiatric and healthy control groups using the UCLA Consortium for Neuropsychiatric Phenomics dataset.

## Project goal

The goal is to explore whether schizophrenia, bipolar disorder, ADHD, and healthy controls show different brain connectivity patterns in resting-state fMRI data.

This project is not intended as a clinical diagnostic tool. It focuses on interpretable neuroimaging analysis, connectome construction, group comparison, and baseline machine learning models.

## Dataset

Dataset: UCLA Consortium for Neuropsychiatric Phenomics / OpenNeuro ds000030.

The dataset includes neuroimaging and behavioral data from healthy controls and participants diagnosed with schizophrenia, bipolar disorder, and ADHD.

## Planned analysis

1. Dataset overview and phenotype exploration.
2. Extraction of regional BOLD time series from resting-state fMRI.
3. Construction of functional connectivity matrices.
4. Group-level comparison of connectivity patterns.
5. Graph-theoretical analysis of brain networks.
6. Baseline machine learning classification.
7. Interpretation of limitations and reproducibility.

## Tech stack

- Python
- NumPy
- Pandas
- Nilearn
- Nibabel
- Scikit-learn
- Matplotlib
- NetworkX
- Jupyter Notebook

## Limitations

This project does not make clinical diagnostic claims. Potential limitations include small sample sizes, head motion artifacts, medication effects, demographic confounds, and limited generalizability.
