#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General operaions on numpy arrays used for cargoat.

@author: earnestt1234
"""

from collections.abc import Iterable

import numpy as np

COLUMN_THRESHOLD = 1000

# n=1, allowed=False, doors<COLUMN_THRESHOLD
# n=1, allowed=False, doors>=COLUMN_THRESHOLD
def _basic_one_per_row_randint(shape2D, dtype=int, **kwargs):
    x, y = shape2D
    output = np.zeros(shape2D, dtype=dtype)
    choices = np.random.randint(low=0, high=y, size=x)
    output[np.arange(x), choices] = 1
    return output

# n=1, allowed=True, doors<COLUMN_THRESHOLD
def _allowed_one_per_row_argmax(shape2D, allowed=None, dtype=int, enforce_allowed=True, **kwargs):
    if allowed is None:
        allowed = np.ones(shape2D, dtype=int)

    output = np.zeros(shape2D, dtype=int)
    weights = np.random.rand(*shape2D) * allowed
    chosen = weights.argmax(1)
    output[np.arange(shape2D[0]), chosen] = 1

    if enforce_allowed:
        output[~allowed.astype(bool)] = 0

    return output

# n>1, allowed=False, doors<COLUMN_THRESHOLD
def _basic_n_per_row_randint(shape2D, n, dtype=int, **kwargs):
    rands = np.random.rand(*shape2D).argsort(1)
    output = (rands < n).astype(int)
    return output

# n>1, allowed=True, doors<COLUMN_THRESHOLD
def _allowed_n_per_row_2argsort(shape2D, n, allowed=None, dtype=int, enforce_allowed=True, **kwargs):
    if allowed is None:
        allowed = np.ones(shape2D, dtype=int)

    output = np.zeros(shape2D, dtype=int)
    weights = np.random.rand(*shape2D) * allowed
    indices = (-weights).argsort(1).argsort(1)
    output[indices < n] = 1

    if enforce_allowed:
        output[~allowed.astype(bool)] = 0

    return output

# n=1, allowed=True, doors>=COLUMN_THRESHOLD
# n>1, allowed=True, doors>=COLUMN_THRESHOLD
def _allowed_n_per_row_choice(shape2D, n, allowed=None, dtype=int, enforce_allowed=True, **kwargs):

    x, y = shape2D

    if allowed is None:
        allowed = np.ones((x, y))

    y_index = np.arange(y)
    weights = allowed.astype(float)
    weights /= weights.sum(axis=1)[:, np.newaxis]
    weights[np.isnan(weights)] = 1
    foo = lambda x: np.random.choice(y_index, size=n, replace=False, p=x)
    choices = np.apply_along_axis(foo, axis=1, arr=weights)
    choices = choices.flatten()
    output = np.zeros(shape2D, dtype=int)
    output[np.repeat(np.arange(x), n), choices] = 1

    if enforce_allowed:
        output[~allowed.astype(bool)] = 0

    return output

# n>1, allowed=False, doors>=COLUMN_THRESHOLD
def _basic_n_per_row_apply(shape2D, n, dtype=int, **kwargs):
    x, y = shape2D
    arr = np.zeros(shape2D, dtype=int)
    arr[:, :] = np.arange(y)
    choices = np.apply_along_axis(np.random.choice, axis=1, arr=arr, size=n, replace=False).flatten()
    output = np.zeros(shape2D, dtype=dtype)
    output[np.repeat(np.arange(x), n), choices] = 1
    return output

def _get_selection_func(n=1, with_allowed=False, many_columns=False):
    not_1 = n != 1
    with_allowed = with_allowed is not None
    options = {
        (False, False, False) : _basic_one_per_row_randint,
        (False, True,  False) : _allowed_one_per_row_argmax,
        (True,  False, False) : _basic_n_per_row_randint,
        (True,  True,  False) : _allowed_n_per_row_2argsort,
        (False, False, True ) : _basic_one_per_row_randint,
        (False, True,  True ) : _allowed_n_per_row_choice,
        (True , False, True ) : _basic_n_per_row_apply,
        (True , True,  True ) : _allowed_n_per_row_choice
        }
    return options[(not_1, with_allowed, many_columns)]


def get_index_success(boolarray2D, i=0):
    '''Get the coordinate index (x,y) of the *ith* `True` in a
    2D boolean array.'''
    return np.asarray(np.where(boolarray2D)).T[i]

def n_per_row(shape2D, n, allowed=None, dtype=int, enforce_allowed=True,
              column_threshold=None):
    '''Generate binary array with n "True" values per row.  Similar to
    `one_per_row()`, but generalized to multiple selections.

    Use `allowed` to mask some cells as being non-selectable.  `enforce_allowed`
    ensures none of the disallowed selections are selected, but can return
    rows with less than `n` selections.

    The `column_threshold` is used to determine the method for generating
    selections.  If `None`, the global `COLUMN_THRESHOLD` is used.  This
    argument was added to try and optimize different selection routines
    depending on the number of columns.  When above the threshold,
    some approaches which are **not** vectorized will be used.'''

    column_threshold = COLUMN_THRESHOLD if column_threshold is None else column_threshold
    many_columns = shape2D[1] >= column_threshold
    func = _get_selection_func(n=n, with_allowed=allowed, many_columns=many_columns)
    output = func(shape2D=shape2D, n=n, dtype=dtype, allowed=allowed, enforce_allowed=enforce_allowed)

    return output

def one_per_row(shape2D, allowed=None, dtype=int, enforce_allowed=True,
                column_threshold=None):
    '''Generate binary array with one "True" value per row.

    Use `allowed` to mask some cells as being non-selectable.  `enforce_allowed`
    ensures none of the disallowed selections are selected, but can return
    rows with no selections.

    The `column_threshold` is used to determine the method for generating
    selections.  If `None`, the global `COLUMN_THRESHOLD` is used.  This
    argument was added to try and optimize different selection routines
    depending on the number of columns.  When above the threshold,
    some approaches which are **not** vectorized will be used.'''

    column_threshold = COLUMN_THRESHOLD if column_threshold is None else column_threshold
    many_columns = shape2D[1] >= column_threshold
    func = _get_selection_func(n=1, with_allowed=allowed, many_columns=many_columns)
    output = func(shape2D=shape2D, n=1, dtype=dtype, allowed=allowed, enforce_allowed=enforce_allowed)

    return output

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
