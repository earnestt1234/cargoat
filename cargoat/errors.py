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