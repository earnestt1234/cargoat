#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 12:24:20 2022

@author: earnestt1234
"""

import numpy as np

from cargoat.actions.base import MontyHallAction

class AddDoors(MontyHallAction):
    def __init__(self, positions):
        self.positions = positions

    def __call__(self, sim):
        foo = lambda a: np.insert(arr=a, obj=self.positions, values=0, axis=1)
        sim.apply_func(foo)

class RemoveDoors(MontyHallAction):
    def __init__(self, positions):
        self.positions = positions

    def __call__(self, sim):
        foo = lambda a: np.delete(arr=a, obj=self.positions, axis=1)
        sim.apply_func(foo)

class RearrangeDoors(MontyHallAction):
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
