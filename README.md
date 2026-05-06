# Psychiatric Brain Connectivity Analysis

Author: Victoria Kupina
Role: Data Analyst / Junior Data Scientist

## Problem Statement

Psychiatric disorders may be associated with differences in functional brain connectivity.

This project explores resting-state fMRI functional connectivity patterns across psychiatric and control groups using the UCLA Consortium for Neuropsychiatric Phenomics dataset.

The goal is to build an educational neuroscience data analysis pipeline, not a clinical diagnostic tool.

## Objectives

- Load and inspect neuroimaging metadata.
- Extract or load functional connectivity matrices.
- Compare brain connectivity patterns across diagnostic groups.
- Perform exploratory statistical testing.
- Apply FDR correction for multiple comparisons.
- Build a simple baseline machine learning classifier.
- Clearly document limitations caused by very small sample size.

## Dataset

This project is based on the UCLA Consortium for Neuropsychiatric Phenomics dataset, available through OpenNeuro as `ds000030`.

The dataset includes participants from several groups, including:

- healthy controls;
- schizophrenia;
- bipolar disorder;
- ADHD.

Large neuroimaging files are not stored in this repository. Local data should be placed in the `data/` directory according to the project instructions.

## Project Structure

- `assets/` — visual assets used in the README.
- `data/` — local raw and processed data directories.
- `notebooks/` — step-by-step analysis notebooks.
- `src/` — reusable Python functions.
- `requirements.txt` — Python dependencies.
- `README.md` — project documentation.
- `LICENSE` — MIT license.

## Methods

- Resting-state fMRI analysis
- ROI-based functional connectivity
- Pearson correlation connectivity matrices
- Group-level connectivity comparison
- Permutation testing
- Benjamini-Hochberg FDR correction
- Baseline machine learning classification
- Leave-One-Out cross-validation for tiny sample demonstration

## Notebooks

| Notebook | Description |
|---|---|
| `01_dataset_overview.ipynb` | Inspect dataset metadata and diagnostic groups |
| `02_connectivity_matrices.ipynb` | Build or load functional connectivity matrices |
| `03_group_connectivity_comparison.ipynb` | Compare connectivity matrices across groups |
| `04_statistical_testing.ipynb` | Run exploratory permutation testing and FDR correction |
| `05_ml_classification.ipynb` | Train a simple baseline classifier on connectivity features |

## Source Code

| File | Description |
|---|---|
| `src/connectivity.py` | Functions for downloading data, extracting ROI time series and computing connectivity matrices |
| `src/statistics.py` | Functions for vectorizing matrices, permutation testing and FDR correction |
| `src/modeling.py` | Functions for baseline machine learning classification |

## Results

The project demonstrates a full exploratory workflow for psychiatric brain connectivity analysis.

Current results should be interpreted cautiously because the repository uses a very small validation subset. The statistical testing and machine learning sections are included to demonstrate methodology, not to make clinical or scientific claims.

## Visual Results

Add generated figures here after running the notebooks, for example:

- group mean connectivity heatmaps;
- connectivity difference heatmaps;
- top altered connections;
- classifier confusion matrix.

## Tech Stack

- Python
- NumPy
- Pandas
- Matplotlib
- SciPy
- Scikit-learn
- Nilearn
- NiBabel
- Jupyter Lab

## How to Run

Clone the repository:

```bash
git clone https://github.com/kva99kva-eng/psychiatric-brain-connectivity-analysis.git
```

Go to the project folder:

```bash
cd psychiatric-brain-connectivity-analysis
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Jupyter Lab:

```bash
jupyter lab
```

Then run the notebooks in order from `01` to `05`.

## Limitations

This project uses a simplified educational workflow and a very small local validation subset.

It does not provide:

- clinical diagnosis;
- validated biomarkers;
- population-level statistical conclusions;
- production-grade neuroimaging preprocessing;
- large-sample model validation;
- medical recommendations.

The statistical and machine learning results should be interpreted as pipeline demonstrations only.

## License

This project is licensed under the MIT License.
