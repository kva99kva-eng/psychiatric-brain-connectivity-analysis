# Transdiagnostic Functional Connectivity Analysis in Psychiatric Disorders

This project analyzes resting-state fMRI functional connectivity patterns across psychiatric diagnostic groups using the UCLA Consortium for Neuropsychiatric Phenomics dataset.

The goal is to explore whether schizophrenia, bipolar disorder, ADHD, and healthy controls show different brain connectivity patterns in resting-state fMRI data.

This project is not intended as a clinical diagnostic tool. It focuses on interpretable neuroimaging analysis, connectome construction, group comparison, exploratory statistical testing, and baseline machine learning workflows.

## Problem Statement

Psychiatric disorders may be associated with altered patterns of functional connectivity between brain regions.

This project demonstrates how resting-state fMRI data can be transformed into ROI-to-ROI connectivity matrices and used for exploratory group comparison and machine learning classification.

## Dataset

Dataset: UCLA Consortium for Neuropsychiatric Phenomics / OpenNeuro ds000030.

The dataset includes neuroimaging and behavioral data from healthy controls and participants diagnosed with schizophrenia, bipolar disorder, and ADHD.

Large raw neuroimaging files are not included in this repository. They should be stored locally in:

`data/raw/`

Processed intermediate files should be stored locally in:

`data/processed/`

## Objectives

- Load and inspect participant-level metadata.
- Select subjects with available resting-state fMRI data.
- Extract regional BOLD time series using a brain atlas.
- Build ROI-to-ROI functional connectivity matrices.
- Compare connectivity patterns across diagnostic groups.
- Run exploratory edge-wise statistical testing.
- Apply multiple-comparison correction.
- Train baseline machine learning classifiers on connectivity features.
- Interpret limitations and avoid clinical overclaiming.

## Project Structure

- `notebooks/01_dataset_overview.ipynb` - dataset overview and participant metadata exploration.
- `notebooks/02_connectivity_matrices.ipynb` - single-subject connectivity matrix construction.
- `notebooks/03_group_connectivity_comparison.ipynb` - group-level connectivity comparison.
- `notebooks/04_statistical_testing.ipynb` - exploratory statistical testing of connectivity differences.
- `notebooks/05_ml_classification.ipynb` - baseline ML classification using connectivity features.
- `src/connectivity.py` - connectivity matrix utilities.
- `src/statistics.py` - statistical testing utilities.
- `src/modeling.py` - machine learning helper functions.
- `data/raw/` - local raw neuroimaging data.
- `data/processed/` - local processed data.
- `reports/` - local analysis outputs and figures.
- `requirements.txt` - Python dependencies.
- `LICENSE` - MIT license.

## Methods

- Resting-state fMRI analysis
- Brain atlas parcellation
- Regional BOLD time series extraction
- Functional connectivity matrix construction
- Group-average connectivity comparison
- Permutation-based statistical testing
- Benjamini-Hochberg FDR correction
- Baseline machine learning classification
- Leakage-safe train/test workflows

## Notebooks

- `01_dataset_overview.ipynb` - explores participant metadata and diagnostic group structure.
- `02_connectivity_matrices.ipynb` - builds a functional connectivity matrix for resting-state fMRI data.
- `03_group_connectivity_comparison.ipynb` - compares average connectivity patterns across diagnostic groups.
- `04_statistical_testing.ipynb` - performs exploratory statistical testing of group-level connectivity differences.
- `05_ml_classification.ipynb` - trains baseline classifiers on functional connectivity features.

## Current Results

The project currently includes five completed analysis stages:

1. Dataset overview and participant-level metadata exploration.
2. Single-subject resting-state fMRI connectivity matrix construction.
3. Small group-level functional connectivity comparison across diagnostic groups.
4. Exploratory statistical testing of connectivity differences.
5. Baseline machine learning classification using functional connectivity features.

Implemented pipeline:

`participant metadata -> resting-state fMRI data -> brain atlas parcellation -> regional BOLD time series -> ROI-to-ROI functional connectivity matrix -> group-average connectivity comparison -> permutation-based statistical testing -> baseline ML classification`

Current outputs include:

- participant-level metadata inspection;
- selection of participants with available resting-state fMRI data;
- extraction of regional BOLD time series using the Harvard-Oxford cortical atlas;
- construction of 48 x 48 ROI-to-ROI functional connectivity matrices;
- exploratory group-average connectivity comparison;
- permutation-based edge-wise statistical testing;
- Benjamini-Hochberg FDR correction;
- baseline multiclass diagnostic classification;
- baseline binary psychiatric-vs-control classification.

## Key Visual Results

### Group-level connectivity differences

Mean functional connectivity difference matrix for the SCHZ vs CONTROL comparison.

![Group connectivity differences](assets/group_connectivity_difference.png)

### Machine learning classification results

Baseline classification result based on functional connectivity features.

![ML classification results](assets/ml_classification_results.png)


## Tech Stack

- Python
- NumPy
- Pandas
- Nilearn
- Nibabel
- SciPy
- scikit-learn
- Matplotlib
- NetworkX
- Jupyter Notebook

## How to Run

Clone the repository:

`git clone https://github.com/kva99kva-eng/psychiatric-brain-connectivity-analysis.git`

Go to the project folder:

`cd psychiatric-brain-connectivity-analysis`

Create and activate a virtual environment:

`python -m venv .venv`

`.venv\Scripts\activate`

Install dependencies:

`pip install -r requirements.txt`

Run Jupyter Lab:

`jupyter lab`

Then run the notebooks in order from `01` to `05`.

## Limitations

This project does not make clinical diagnostic claims.

The current analysis should be interpreted as an exploratory technical demonstration. Important limitations include:

- small sample size;
- head motion artifacts;
- medication effects;
- demographic confounds;
- preprocessing and denoising choices;
- limited generalizability;
- potential instability of statistical and ML results on small samples.

## Future Work

- Increase the number of subjects per diagnostic group.
- Add confound regression using fMRIPrep confounds.
- Compare multiple brain atlases.
- Add graph-theoretical network metrics.
- Add feature importance analysis for machine learning models.
- Improve visual reporting of group-level connectivity differences.
- Add more robust validation for classification workflows.

## License

This project is licensed under the MIT License.
