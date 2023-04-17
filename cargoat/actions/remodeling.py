#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Actions for changing the number or arrangement of doors.
"""

import numpy as np

from cargoat.actions.base import MontyHallAction

class AddDoors(MontyHallAction):
    def __init__(self, positions):
        '''
        Add additional doors at desired positions within the simulation.
        Doors will be unpicked, closed, and containing goats.

        Parameters
        ----------
        positions : list-like
            Positions to add doors.  See `np.insert` for more details.

        Returns
        -------
        None.

        '''
        self.positions = positions

    def __call__(self, sim):
        foo = lambda a: np.insert(arr=a, obj=self.positions, values=0, axis=1)
        sim.apply_func(foo)
        return sim

class RemoveDoors(MontyHallAction):
    def __init__(self, positions):
        '''
        Remove selected doors from the simulation, based on index.

        Parameters
        ----------
        positions : list-like
            Doors to remove.  See `np.remove` for more details.

        Returns
        -------
        None.

        '''
        self.positions = positions

    def __call__(self, sim):
        tolist = [self.positions] if type(self.positions) in [float, int] else self.positions
        if set(tolist) == set(range(sim.shape[1])):
            sim.make_empty()
        else:
            foo = lambda a: np.delete(arr=a, obj=self.positions, axis=1)
            sim.apply_func(foo)
        return sim

class RearrangeDoors(MontyHallAction):
    def __init__(self, positions):
        '''
        Swap the positions of doors.  Note that the contents, picked-status,
        and revealed-status all stick with the door.

        Parameters
        ----------
        positions : list-like
            Permutation of the range of the number of doors, dictating
            the new position of each door.

        Returns
        -------
        None.

        '''
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
        return sim
