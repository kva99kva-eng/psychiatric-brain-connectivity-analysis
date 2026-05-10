import numpy as np
import pandas as pd

from src.connectivity import (
    compute_connectivity_matrix,
    get_subject_func_filename,
    get_subject_func_path,
    save_connectivity_matrix,
)


def test_get_subject_func_filename():
    filename = get_subject_func_filename("sub-10159")

    assert filename == "sub-10159_task-rest_bold_space-MNI152NLin2009cAsym_preproc.nii.gz"


def test_get_subject_func_path_uses_expected_structure(tmp_path):
    path = get_subject_func_path("sub-10159", raw_dir=tmp_path)

    assert path.name == "sub-10159_task-rest_bold_space-MNI152NLin2009cAsym_preproc.nii.gz"
    assert path.parent.name == "func"
    assert path.parent.parent.name == "sub-10159"


def test_save_connectivity_matrix_creates_npy_and_csv(tmp_path):
    matrix = np.array(
        [
            [0.0, 0.1],
            [0.1, 0.0],
        ]
    )
    roi_labels = ["ROI_1", "ROI_2"]

    npy_path, csv_path = save_connectivity_matrix(
        matrix=matrix,
        roi_labels=roi_labels,
        subject_id="sub-test",
        output_dir=tmp_path,
    )

    assert npy_path.exists()
    assert csv_path.exists()

    loaded_matrix = np.load(npy_path)
    loaded_df = pd.read_csv(csv_path, index_col=0)

    assert np.allclose(loaded_matrix, matrix)
    assert list(loaded_df.index) == roi_labels
    assert list(loaded_df.columns) == roi_labels


def test_compute_connectivity_matrix_returns_square_matrix_with_zero_diagonal():
    rng = np.random.default_rng(42)
    time_series = rng.normal(size=(30, 4))

    matrix = compute_connectivity_matrix(time_series)

    assert matrix.shape == (4, 4)
    assert np.allclose(np.diag(matrix), 0.0)
    assert np.allclose(matrix, matrix.T)
