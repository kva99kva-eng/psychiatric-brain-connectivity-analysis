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

* Python
* NumPy
* Pandas
* Nilearn
* Nibabel
* Scikit-learn
* Matplotlib
* NetworkX
* Jupyter Notebook

## Limitations

This project does not make clinical diagnostic claims. Potential limitations include small sample sizes, head motion artifacts, medication effects, demographic confounds, and limited generalizability.



\## Current progress



## Current progress

The project currently includes five completed analysis stages:

1. Dataset overview and participant-level metadata exploration.
2. Single-subject resting-state fMRI connectivity matrix construction.
3. Small group-level functional connectivity comparison across diagnostic groups.
4. Exploratory statistical testing of connectivity differences.
5. Baseline machine learning classification using functional connectivity features.

Implemented pipeline:

```text
participant metadata
→ resting-state fMRI data
→ brain atlas parcellation
→ regional BOLD time series
→ ROI-to-ROI functional connectivity matrix
→ group-average connectivity comparison
→ permutation-based statistical testing
→ baseline ML classification

Current results
Loaded participant-level metadata from the UCLA CNP dataset.
Selected participants with available resting-state fMRI data.
Extracted regional BOLD time series using the Harvard-Oxford cortical atlas.
Built 48 × 48 ROI-to-ROI functional connectivity matrices.
Extended the pipeline from one subject to a small multi-group diagnostic sample.
Computed average connectivity matrices for diagnostic groups.
Performed exploratory permutation-based edge-wise statistical testing.
Applied Benjamini-Hochberg FDR correction.
Built baseline leakage-safe ML classification workflows using functional connectivity features.
Evaluated both multiclass diagnostic classification and binary psychiatric-vs-control classification.
Important limitations

This project does not make clinical diagnostic claims. The current sample size is intentionally small and used for pipeline validation. Statistical and ML results should be interpreted as exploratory technical demonstrations, not as scientific or clinical conclusions.

Potential limitations include:

small sample size;
head motion artifacts;
medication effects;
demographic confounds;
preprocessing and denoising choices;
limited generalizability.
Next steps

Planned improvements:

Increase the number of subjects per diagnostic group.
Add fMRIPrep confound regression.
Compare multiple brain atlases.
Add graph-theoretical network metrics.
Add feature importance analysis for ML models.
Improve visual reporting of group-level connectivity differences.


Repository structure

psychiatric-brain-connectivity-analysis/

│

├── notebooks/

│   ├── 01\_dataset\_overview.ipynb

│   ├── 02\_connectivity\_matrices.ipynb

│   └── 03\_group\_connectivity\_comparison.ipynb

│

├── src/

│   ├── \_\_init\_\_.py

│   ├── connectivity.py

│   ├── data\_loading.py

│   ├── modeling.py

│   └── visualization.py

│

├── data/

│   ├── raw/

│   └── processed/

│

├── reports/

│   └── figures/

│

├── README.md

├── requirements.txt

└── .gitignore

Next steps



Planned improvements:



Increase the number of subjects per diagnostic group.

Add confound regression using fMRIPrep confounds.

Add statistical testing of group-level connectivity differences.

Apply multiple-comparison correction.

Train baseline machine learning models on connectivity features.

Add interpretation of the most informative brain connections.

## Current progress

The project currently includes three completed analysis stages:

1. Dataset overview and participant-level metadata exploration.
2. Single-subject resting-state fMRI connectivity matrix construction.
3. Small group-level functional connectivity comparison across diagnostic groups.

Implemented pipeline:

```text
participant metadata
→ resting-state fMRI data
→ brain atlas parcellation
→ regional BOLD time series
→ ROI-to-ROI functional connectivity matrix
→ group-average connectivity comparison

Current results
Loaded participant-level metadata from the UCLA CNP dataset.
Selected participants with available resting-state fMRI data.
Extracted regional BOLD time series using the Harvard-Oxford cortical atlas.
Built 48 × 48 ROI-to-ROI functional connectivity matrices.
Extended the pipeline from one subject to a small multi-group diagnostic sample.
Computed average connectivity matrices for diagnostic groups.
Visualized preliminary group-level connectivity differences.

psychiatric-brain-connectivity-analysis/
│
├── notebooks/
│   ├── 01_dataset_overview.ipynb
│   ├── 02_connectivity_matrices.ipynb
│   └── 03_group_connectivity_comparison.ipynb
│
├── src/
│   ├── __init__.py
│   ├── connectivity.py
│   ├── data_loading.py
│   ├── modeling.py
│   └── visualization.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── reports/
│   └── figures/
│
├── README.md
├── requirements.txt
└── .gitignore
Next steps

Planned improvements:

Increase the number of subjects per diagnostic group.
Add confound regression using fMRIPrep confounds.
Add statistical testing of group-level connectivity differences.
Apply multiple-comparison correction.
Train baseline machine learning models on connectivity features.
Add interpretation of the most informative brain connections.