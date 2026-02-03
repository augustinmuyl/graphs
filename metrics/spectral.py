# L, Lsym, Lrw + lambda2, lambda_n, lambda_n/lambda2, optional Kirchhoff

import numpy as np
import networkx as nx
from scipy.sparse.linalg import eigsh

## Laplacians


def combinatorial_laplacian(G):
    return nx.laplacian_matrix(G).astype(float)


def symmetric_normalized_laplacian(G):
    return nx.normalized_laplacian_matrix(G).astype(float)


def random_walk_normalized_laplacian(G):
    return nx.directed_laplacian_matrix(G, walk_type="random").astype(float)


## Spectral properties


def algebraic_connectivity(G):
    return nx.algebraic_connectivity(G)


def fiedler_vector(G):
    return nx.fiedler_vector(G)


def _lambda2_from_laplacian(L):
    n = L.shape[0]
    if n <= 1000:
        eigenvalues = np.linalg.eigvalsh(L.toarray())
        return eigenvalues[1]
    return eigsh(L, k=2, which="SM", return_eigenvectors=False)[1]


def _largest_eigenvalue(L):
    n = L.shape[0]
    if n <= 1000:
        eigenvalues = np.linalg.eigvalsh(L.toarray())
        return eigenvalues[-1]
    return eigsh(L, k=1, which="LA", return_eigenvectors=False)[0]


def spectral_gap_ratio(G):
    L = combinatorial_laplacian(G)
    lambda2 = _lambda2_from_laplacian(L)
    lambda_n = _largest_eigenvalue(L)
    return lambda_n / lambda2


def kirchhoff_index(G, max_n=1000):
    L = combinatorial_laplacian(G)
    n = L.shape[0]
    if n > max_n:
        raise ValueError(
            f"Kirchhoff index is O(n^3) with dense eigendecomposition; n={n} exceeds max_n={max_n}."
        )
    eigenvalues = np.linalg.eigvalsh(L.toarray())
    non_zero_eigenvalues = eigenvalues[1:]  # Exclude the zero eigenvalue
    return n * np.sum(1.0 / non_zero_eigenvalues)
