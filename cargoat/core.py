#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core functions for doing things in cargoat.
"""

import numpy as np

from cargoat.errors import MontyHallError
from cargoat.sim import MontyHallSim

def play(game, n=100, seed=None):
    '''
    Run a MontyHall simulation.

    Parameters
    ----------
    game : list-like
        A list of objects from the `cargoat.actions` subpackage.
    n : int, optional
        Number of games to simulate. The default is 100.
    seed: number, optional
        Set the seed for the RNG.  See numpy docs for more information.

    Raises
    ------
    MontyHallError
        Problem with completing the game.

    Returns
    -------
    sim : MontyHallSim
        Simulation object, recording the trials and results.

    '''
    if seed:
        np.random.seed(seed)

    sim = MontyHallSim(n=n)
    for i, action in enumerate(game):
        try:
            action(sim)
        except Exception as error:
            msg = f'Error for step {i}: {repr(action)}'
            raise MontyHallError(msg) from error

    return sim
