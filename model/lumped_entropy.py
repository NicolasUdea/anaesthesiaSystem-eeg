# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 11:12:33 2022

@author: Maria Camila Villa, Yeimmy Morales
"""

import numpy as np
from math import factorial


def _embed(x, order=3, delay=1):
    """Time-delay embedding.
    Parameters
    ----------
    x : 1d-array, shape (n_times)
        Time series
    order : int
        Embedding dimension (order)
    delay : int
        Delay.
    Returns
    -------
    y : ndarray, shape (n_times - (order - 1) * delay, order)
        transposed embedded time-series.
    """
    n = len(x)
    y = np.empty((order, n-(order-1)*delay))
    for i in range(order):
        y[i] = x[i*delay:i*delay+y.shape[1]]
    return y.T


def split_matrix(matrix, order=3):
    """
    Organize a matrix in descendng order, then splits the matrix by columns.

    To use:
    >>> matrix = [[4, 7, 9], [7, 9, 10], [9, 10, 6]]
    >>> vectors = split_matrix(matrix, 3)
    [array([[9], [10], [10]]), array([[7], [9], [9]]), array([[4], [7], [6]])]

    Parameters
    ----------
    matrix : ndarray, shape (n, order)
        array to be split.
    order : int, optional
        matrix's number of columns. The default is 3.

    Returns
    -------
    vectors : ndarray
        split array.

    """
    matrix = -np.sort(-matrix, axis=1)
    vectors = np.hsplit(matrix, order)
    return vectors


def lumped_idx(matrix):
    """
    Substracts vectors by column.

    To use:
    >>> matrix = [array([[9], [10], [10]]), array([[7], [9], [9]]),
                  array([[4], [7], [6]])]
    >>> substract_vector = lumped_idx(matrix)
    array([[2, 1, 1], [3, 2, 3]])

    Parameters
    ----------
    matrix : ndarray
        array to be substract.

    Returns
    -------
    substract_vector : ndarray
        substracted array.

    """
    substract_vector = np.empty((len(matrix)-1, len(matrix[0])))
    for i in range(len(matrix)-1):
        substract_vector[i] = np.squeeze(matrix[i]-matrix[i+1])
    return np.abs(substract_vector)


def lumped_permutation(matrix, sorted_idx, threshold=1):
    """
    Compare the matrix substract_vector with the threshold, if this value is
    less than the threshold 1 is subtracted from the entire row of the matrix

    Parameters
    ----------
    matrix : ndarray
        matrix with the substracted values to be compare.
    sorted_idx : ndarray
        matrix with the rank order pattern.
    threshold : int, optional
        the default is 1.

    Returns
    -------
    lump_perm : ndarray
        rank order pattern of lumped permutation entropy.

    """
    lump_perm = sorted_idx
    for j in range(len(matrix)):
        for i in range(len(matrix[0])):
            if matrix[j, i] < threshold:
                lump_perm[i] = sorted_idx[i]-1
    lump_perm[lump_perm < 0] = 0
    return lump_perm


def lumped_permutation_entropy(time_series, order=3, delay=1, normalize=True):
    """
    Receive a time series and return the compute lumped permutation entropy

    Parameters
    ----------
    time_series : ndarray
        .
    order : int, optional
        the embedding dimension. The default is 3.
    delay : int, optional
        the embedding time delay. The default is 1.
    normalize : bool, optional
        if true the lumped permutation entropy is normalize.
        The default is True.

    Returns
    -------
    pe : float
        compute lumped permutation entropy.

    """
    x = np.array(time_series)
    hashmult = np.power(order, np.arange(order))
    # Embed x and sort the order of permutations
    sorted = _embed(x, order=order, delay=delay).astype(int)
    sorted_idx = np.argsort(np.argsort(-sorted))
    matrix = split_matrix(sorted, order=3)
    lumped_matrix = lumped_idx(matrix)
    lumped_permut = lumped_permutation(lumped_matrix, sorted_idx, threshold=1)

    # Associate unique integer to each permutations
    hashval = (np.multiply(lumped_permut, hashmult)).sum(1)
    # Return the counts
    _, c = np.unique(hashval, return_counts=True)
    # Use np.true_divide for Python 2 compatibility
    p = np.true_divide(c, c.sum())
    pe = -np.multiply(p, np.log2(p)).sum()
    if normalize:
        pe /= np.log2(factorial(order))
    return pe
