import numpy as np

from src.statistics import (
    benjamini_hochberg_fdr,
    reconstruct_symmetric_matrix,
    vectorize_upper_triangle,
)


def test_vectorize_upper_triangle_returns_expected_values():
    matrix = np.array(
        [
            [0.0, 0.1, 0.2],
            [0.1, 0.0, 0.3],
            [0.2, 0.3, 0.0],
        ]
    )

    vector, triu_indices = vectorize_upper_triangle(matrix)

    assert vector.shape == (3,)
    assert np.allclose(vector, np.array([0.1, 0.2, 0.3]))
    assert len(triu_indices) == 2


def test_reconstruct_symmetric_matrix_from_vector():
    vector = np.array([0.1, 0.2, 0.3])
    triu_indices = np.triu_indices(3, k=1)

    matrix = reconstruct_symmetric_matrix(
        vector=vector,
        triu_indices=triu_indices,
        matrix_size=3,
    )

    expected = np.array(
        [
            [0.0, 0.1, 0.2],
            [0.1, 0.0, 0.3],
            [0.2, 0.3, 0.0],
        ]
    )

    assert matrix.shape == (3, 3)
    assert np.allclose(matrix, expected)


def test_benjamini_hochberg_fdr_output_shape_and_range():
    p_values = np.array([0.001, 0.02, 0.20, 0.80])

    rejected, adjusted_p_values = benjamini_hochberg_fdr(
        p_values=p_values,
        alpha=0.05,
    )

    assert rejected.shape == p_values.shape
    assert adjusted_p_values.shape == p_values.shape
    assert adjusted_p_values.min() >= 0
    assert adjusted_p_values.max() <= 1
    assert rejected.dtype == bool
