from pathlib import Path
from urllib.request import urlretrieve

import numpy as np
import pandas as pd

from nilearn import datasets
from nilearn.maskers import NiftiLabelsMasker
from nilearn.connectome import ConnectivityMeasure


def get_project_root() -> Path:
    """
    Return project root assuming this file is located in src/.
    """
    return Path(__file__).resolve().parents[1]


def get_subject_func_filename(subject_id: str) -> str:
    """
    Return expected fMRIPrep resting-state fMRI filename for ds000030.
    """
    return f"{subject_id}_task-rest_bold_space-MNI152NLin2009cAsym_preproc.nii.gz"


def get_subject_func_path(subject_id: str, raw_dir: Path | None = None) -> Path:
    """
    Return local path for a subject's preprocessed resting-state fMRI file.
    """
    project_root = get_project_root()

    if raw_dir is None:
        raw_dir = project_root / "data" / "raw"

    filename = get_subject_func_filename(subject_id)

    return raw_dir / subject_id / "func" / filename


def download_preprocessed_rest_fmri(
    subject_id: str,
    raw_dir: Path | None = None,
    overwrite: bool = False,
) -> Path:
    """
    Download one preprocessed resting-state fMRI file from OpenNeuro S3.

    Parameters
    ----------
    subject_id:
        Subject ID, for example 'sub-10159'.
    raw_dir:
        Local raw data directory.
    overwrite:
        If True, download even if the file already exists.

    Returns
    -------
    Path to downloaded or existing file.
    """
    func_path = get_subject_func_path(subject_id, raw_dir=raw_dir)
    func_path.parent.mkdir(parents=True, exist_ok=True)

    if func_path.exists() and not overwrite:
        print(f"File already exists: {func_path}")
        return func_path

    filename = get_subject_func_filename(subject_id)

    candidate_urls = [
        f"https://s3.amazonaws.com/openneuro/ds000030/ds000030_R1.0.4/uncompressed/derivatives/fmriprep/{subject_id}/func/{filename}",
        f"https://s3.amazonaws.com/openneuro/ds000030/ds000030_R1.0.5/uncompressed/derivatives/fmriprep/{subject_id}/func/{filename}",
    ]

    last_error = None

    for url in candidate_urls:
        try:
            print(f"Trying download from: {url}")
            urlretrieve(url, func_path)
            print(f"Downloaded to: {func_path}")
            return func_path
        except Exception as error:
            last_error = error
            print(f"Failed: {error}")

    raise RuntimeError(f"Could not download file for {subject_id}. Last error: {last_error}")


def load_harvard_oxford_atlas():
    """
    Load Harvard-Oxford cortical atlas.

    Returns
    -------
    atlas_filename:
        Path to atlas image.
    roi_labels:
        ROI labels excluding background.
    """
    atlas = datasets.fetch_atlas_harvard_oxford(
        atlas_name="cort-maxprob-thr25-2mm"
    )

    atlas_filename = atlas.maps
    roi_labels = atlas.labels[1:]

    return atlas_filename, roi_labels


def extract_roi_time_series(
    func_path: Path | str,
    atlas_filename,
    t_r: float = 2.0,
    low_pass: float = 0.1,
    high_pass: float = 0.01,
) -> np.ndarray:
    """
    Extract regional BOLD time series using a labels atlas.
    """
    masker = NiftiLabelsMasker(
        labels_img=atlas_filename,
        standardize="zscore_sample",
        detrend=True,
        low_pass=low_pass,
        high_pass=high_pass,
        t_r=t_r,
        verbose=0,
    )

    time_series = masker.fit_transform(str(func_path))

    return time_series


def compute_connectivity_matrix(time_series: np.ndarray) -> np.ndarray:
    """
    Compute ROI-to-ROI Pearson correlation matrix.
    """
    correlation_measure = ConnectivityMeasure(
        kind="correlation",
        standardize="zscore_sample",
    )

    matrix = correlation_measure.fit_transform([time_series])[0]

    np.fill_diagonal(matrix, 0)

    return matrix


def save_connectivity_matrix(
    matrix: np.ndarray,
    roi_labels: list[str],
    subject_id: str,
    output_dir: Path | None = None,
) -> tuple[Path, Path]:
    """
    Save connectivity matrix as .npy and .csv.
    """
    project_root = get_project_root()

    if output_dir is None:
        output_dir = project_root / "data" / "processed" / "connectivity"

    output_dir.mkdir(parents=True, exist_ok=True)

    npy_path = output_dir / f"{subject_id}_connectivity_matrix.npy"
    csv_path = output_dir / f"{subject_id}_connectivity_matrix.csv"

    np.save(npy_path, matrix)

    matrix_df = pd.DataFrame(
        matrix,
        index=roi_labels,
        columns=roi_labels,
    )

    matrix_df.to_csv(csv_path)

    return npy_path, csv_path


def build_subject_connectivity_matrix(subject_id: str) -> dict:
    """
    Full single-subject pipeline:

    download fMRI -> load atlas -> extract time series -> compute matrix -> save matrix.
    """
    func_path = download_preprocessed_rest_fmri(subject_id)
    atlas_filename, roi_labels = load_harvard_oxford_atlas()

    time_series = extract_roi_time_series(
        func_path=func_path,
        atlas_filename=atlas_filename,
    )

    matrix = compute_connectivity_matrix(time_series)

    npy_path, csv_path = save_connectivity_matrix(
        matrix=matrix,
        roi_labels=roi_labels,
        subject_id=subject_id,
    )

    return {
        "subject_id": subject_id,
        "func_path": func_path,
        "time_series_shape": time_series.shape,
        "matrix_shape": matrix.shape,
        "npy_path": npy_path,
        "csv_path": csv_path,
    }