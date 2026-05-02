import numpy as np
import pandas as pd


def vectorize_upper_triangle(matrix: np.ndarray) -> tuple[np.ndarray, tuple[np.ndarray, np.ndarray]]:
    """
    Convert a square connectivity matrix into a vector using the upper triangle.
    Diagonal is excluded.
    """
    triu_indices = np.triu_indices_from(matrix, k=1)
    vector = matrix[triu_indices]
    return vector, triu_indices


def reconstruct_symmetric_matrix(
    vector: np.ndarray,
    triu_indices: tuple[np.ndarray, np.ndarray],
    matrix_size: int,
) -> np.ndarray:
    """
    Reconstruct a symmetric matrix from an upper-triangle vector.
    """
    matrix = np.zeros((matrix_size, matrix_size))
    matrix[triu_indices] = vector
    matrix = matrix + matrix.T
    return matrix


def benjamini_hochberg_fdr(p_values: np.ndarray, alpha: float = 0.05) -> tuple[np.ndarray, np.ndarray]:
    """
    Benjamini-Hochberg FDR correction.
    """
    p_values = np.asarray(p_values)
    n_tests = len(p_values)

    sorted_indices = np.argsort(p_values)
    sorted_p = p_values[sorted_indices]

    adjusted_sorted = sorted_p * n_tests / np.arange(1, n_tests + 1)
    adjusted_sorted = np.minimum.accumulate(adjusted_sorted[::-1])[::-1]
    adjusted_sorted = np.clip(adjusted_sorted, 0, 1)

    adjusted_p_values = np.empty(n_tests)
    adjusted_p_values[sorted_indices] = adjusted_sorted

    rejected = adjusted_p_values < alpha

    return rejected, adjusted_p_values


def permutation_group_comparison(
    control_vectors: np.ndarray,
    patient_vectors: np.ndarray,
    roi_labels: list[str],
    triu_indices: tuple[np.ndarray, np.ndarray],
    n_permutations: int = 1000,
    alpha: float = 0.05,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Perform edge-wise permutation testing between control and patient connectivity vectors.

    This avoids assumptions of normality and works as an exploratory method for small samples.
    """
    rng = np.random.default_rng(random_state)

    control_vectors = np.asarray(control_vectors)
    patient_vectors = np.asarray(patient_vectors)

    mean_control = np.nanmean(control_vectors, axis=0)
    mean_patient = np.nanmean(patient_vectors, axis=0)

    observed_difference = mean_patient - mean_control
    observed_abs_difference = np.abs(observed_difference)

    combined = np.vstack([control_vectors, patient_vectors])
    n_control = control_vectors.shape[0]
    n_total = combined.shape[0]

    permutation_counts = np.zeros_like(observed_abs_difference, dtype=float)

    for _ in range(n_permutations):
        shuffled_indices = rng.permutation(n_total)

        perm_control = combined[shuffled_indices[:n_control]]
        perm_patient = combined[shuffled_indices[n_control:]]

        perm_difference = np.nanmean(perm_patient, axis=0) - np.nanmean(perm_control, axis=0)
        perm_abs_difference = np.abs(perm_difference)

        permutation_counts += perm_abs_difference >= observed_abs_difference

    p_values = (permutation_counts + 1) / (n_permutations + 1)

    rejected, adjusted_p_values = benjamini_hochberg_fdr(p_values, alpha=alpha)

    roi_i = triu_indices[0]
    roi_j = triu_indices[1]

    results = pd.DataFrame({
        "roi_1": [roi_labels[i] for i in roi_i],
        "roi_2": [roi_labels[j] for j in roi_j],
        "mean_control": mean_control,
        "mean_patient": mean_patient,
        "mean_difference": observed_difference,
        "abs_mean_difference": observed_abs_difference,
        "p_value_permutation": p_values,
        "p_fdr": adjusted_p_values,
        "significant_fdr": rejected,
    })

    return results.sort_values("abs_mean_difference", ascending=False).reset_index(drop=True)