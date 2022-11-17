#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes for individual game rules applied to `MontyHallSim` objects.
"""

from collections.abc import Iterable
import pprint

import numpy as np

from cargoat.arrayops import (one_per_row,
                              one_per_row_weighted,
                              n_per_row)
from cargoat.errors import (BadClose, BadReveal, bad_trials_raise)

# ---- Initialization
class InitDoorsFixed:
    def __init__(self, placement=[0, 0, 1]):
        self.placement = np.array(placement).astype(int)

    def __call__(self, sim):
        shape = (sim.n, len(self.placement))
        sim.cars = np.tile(self.placement, (sim.n, 1))
        sim.picked = np.zeros(shape, dtype=int)
        sim.revealed = np.zeros(shape, dtype=int)
        sim.spoiled = np.zeros(sim.n, dtype=int)

class InitDoorsRandom:
    def __init__(self, cars=1, goats=2):
        self.cars = cars
        self.goats = goats

    def __call__(self, sim):
        shape = (sim.n, self.cars + self.goats)
        sim.cars = np.zeros(shape, dtype=int)
        sim.picked = np.zeros(shape, dtype=int)
        sim.revealed = np.zeros(shape, dtype=int)
        sim.spoiled = np.zeros(sim.n, dtype=int)

        p = np.random.rand(shape[0], shape[1]).argsort(1)
        sim.cars[p < self.cars] = 1

# ---- Generic

# ---- Picking Doors

# class Stay:
#     def __call__(self, sim):
#         pass

# class Switch:
#     def __call__(self, sim):
#         PickDoor()(sim)

# ---- Revealing Doors

# ---- Closing Doors

# ---- Adding & Removing Doors

class AddDoors:
    def __init__(self, positions):
        self.positions = positions

    def __call__(self, sim):
        foo = lambda a: np.insert(arr=a, obj=self.positions, values=0, axis=1)
        sim.apply_func(foo)

class RemoveDoors:
    def __init__(self, positions):
        self.positions = positions

    def __call__(self, sim):
        foo = lambda a: np.delete(arr=a, obj=self.positions, axis=1)
        sim.apply_func(foo)

# ---- Rearranging Doors

class RearrangeDoors:
    def __init__(self, positions):
        self.positions = positions

    def __call__(self, sim):
        col_range = list(range(sim.shape[1]))
        a = np.all(np.isin(col_range, self.positions))
        b = len(col_range) == len(self.positions)
        if not a or not b:
            raise ValueError("Positions must be a permutation of "
                              f"the column indices, i.e. {col_range}.")

        foo = lambda a: a.copy()[:, self.positions]
        sim.apply_func(foo)

# ---- Other
class Finish:
    def __call__(self, sim):
        pprint.pprint(sim.get_results(), sort_dicts=False)
