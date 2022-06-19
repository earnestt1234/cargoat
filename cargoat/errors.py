#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom error types for cargoat.
"""

import numpy as np

class MontyHallError(Exception):
    """Custom Exception for general Monty Hall game violations."""

class BadPick(MontyHallError):
    """Exception indicating a player's door choice violated the game rules,
    typically that an open door was selected."""

class BadReveal(MontyHallError):
    """Exception indicating a door reveal violated the game rules, which could
    mean many things (a car was revealed, there were no goats to reveal,
    a picked door was revealed, etc.)"""

def bad_trials_raise(badrows, msg, errortype):
    '''Typical cargoat error message, saying what went wrong during
    the simulation, and on which rows.'''
    with np.printoptions(threshold=100):
        idx = np.arange(len(badrows))[badrows]
        n = len(idx)
        raise errortype(f"{msg} Found for {n} trial(s):\n{idx}")

def check_n_per_row(a, n, etype, emessage=None, include_eg=True):
    '''Check that a boolean/binary array has a given sum of True values
    per row.  Call `bad_trials_raise()` when condition is not met for all.'''
    if emessage is None:
        emessage = "Incorrect number of selections for some trials."
    n_per_row = a.astype(int).sum(axis=1)
    wrong_n = (n_per_row != n)
    if np.any(wrong_n):
        if include_eg:
            idx = np.argmax(wrong_n) # finds first true
            val = n_per_row[idx]
            emessage += f" E.g. on row {idx}, got {val} but expected {n}."
        bad_trials_raise(wrong_n, emessage, etype)

