#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General operaions on numpy arrays used for cargoat.

@author: earnestt1234
"""

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
