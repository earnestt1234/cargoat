#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General operaions on numpy arrays used for cargoat.

@author: earnestt1234
"""

from collections.abc import Iterable

import numpy as np

def get_index_success(boolarray2D, i=0):
    '''Get the coordinate index (x,y) of the *ith* `True` in a
    2D boolean array.'''
    return np.asarray(np.where(boolarray2D)).T[i]

def n_per_row(shape2D, n, allowed=None, dtype=int, enforce_allowed=True):
    '''Generate binary array with n "True" values per row.  Similar to
    `one_per_row()`, but generalized to multiple selections.

    Use `allowed` to mask some cells as being non-selectable.  `enforce_allowed`
    ensures none of the disallowed selections are selected, but can return
    rows with less than `n` selections.

    The implementation is relatively slow compared to `one_per_row()`.  It
    generates random values of size `shape2D`, then uses a double argsort
    to find the indices of the smallest `n` values.  The double argsort
    scales poorly compared to other options, but seems to give comprable
    or better performance for (approximately) less than 1,000,000 rows.'''

    if allowed is None:
        allowed = np.ones(shape2D, dtype=int)

    output = np.zeros(shape2D, dtype=int)
    weights = np.random.rand(*shape2D) * allowed
    indices = (-weights).argsort(1).argsort(1)
    output[indices < n] = 1

    if enforce_allowed:
        output[~allowed.astype(bool)] = 0

    return output.astype(dtype)

def one_per_row(shape2D, allowed=None, dtype=int, enforce_allowed=True):
    '''Generate binary array with one "True" value per row.

    Use `allowed` to mask some cells as being non-selectable.  `enforce_allowed`
    ensures none of the disallowed selections are selected, but can return
    rows with no selections.'''

    if allowed is None:
        allowed = np.ones(shape2D, dtype=int)

    output = np.zeros(shape2D, dtype=int)
    weights = np.random.rand(*shape2D) * allowed
    chosen = weights.argmax(1)
    output[np.arange(shape2D[0]), chosen] = 1

    if enforce_allowed:
        output[~allowed.astype(bool)] = 0

    return output.astype(dtype)

def one_per_row_weighted(shape2D, weights, allowed=None, dtype=int):
    '''Generate a binary/boolean array with one True per row, where
    the probabilities for each column are weighted.  Similar to
    `one_per_row()`, but allows for custom weighting.

    Weights must either be the same length as the number of columns,
    or the same length as there are "allowed" cells for each row.

    Use `allowed` to mask some cells as being non-selectable.  Having no
    allowed cells for a given row or all 0 weights will throw an error.'''

    w = weights
    n, d = shape2D

    # init empty weights
    wmat = np.full(shape2D, np.nan)

    # unweight if desired
    if allowed is None:
        allowed = np.ones(shape2D, dtype=bool)
    wmat[~allowed] = 0

    # fill in provided weights
    if isinstance(w, Iterable) and len(w) == d:
        wmat = np.where(np.isnan(wmat),
                        np.tile(w, (n, 1)),
                        wmat)
    elif isinstance(w, Iterable):
        lw = len(w)
        spots = np.sum(np.isnan(wmat), axis=1)
        if ~ np.all(spots == lw):
            raise ValueError(f"Number of weights ({lw}) does not match number of open spots "
                             f"for some rows.")
        wmat[np.isnan(wmat)] = np.tile(w, n)

    wsum = np.sum(wmat, axis=1)
    if np.any(wsum == 0):
        raise ValueError("Weights sum to zero.")

    # convert to probabilities
    pmat = wmat / wsum[:, np.newaxis]

    cum_p = np.cumsum(pmat, axis=1)
    draws = np.random.rand(n, 1)
    lt = (cum_p < draws)
    chosen = lt.sum(axis=1)

    output = np.zeros(shape2D, dtype=int)
    output[np.arange(n), chosen] = 1
    return output
