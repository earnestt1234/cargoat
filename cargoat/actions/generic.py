#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generic class to capture picking/unpicking, revealing/closing, and
placing/removing cars.
"""

from collections.abc import Iterable

import numpy as np

from cargoat.actions.base import MontyHallAction
from cargoat.arrayops import (n_per_row,
                              one_per_row,
                              one_per_row_weighted)

class GenericAction(MontyHallAction):
    def __init__(self, target, doors=1, weighted=False, behavior='overwrite',
                 exclude_picked=False, exclude_revealed=False, exclude_cars=False,
                 exclude_unpicked=False,exclude_closed=False, exclude_carless=False,
                 allow_spoiled=False, allow_redundant=True):
        '''
        Generic class for covering many actions in the Monty Hall game.

        Most boil down to altering the cars, picked, or revealed array
        of the MontyHallSim.  This class abstracts the specific array being
        targeted,  allowing the same selection operations to be applied.

        This action covers selecting 1 or more doors with uniform probability,
        selecting 1 or more doors by index, or selecting one door with
        weighted probabilities for each door.

        This class is intended to cover picking, revealing, and placing cars,
        as well as the negation of those actions.  Subclasses of this class
        tailor/mask some of the options from GenericAction where appropriate.
        See `cargoat.actions.pick`, `cargoat.actions.reveal`, and
        `cargoat.actions.car` for more information.

        Parameters
        ----------
        target : 'cars', 'picked', or 'revealed'
            Attribute array of `cargoat.sim.MontyHallSim` to target.
        doors : int or list-like, optional
            Argument for specifying how many/which doors to place cars behind.
            The default is 1. Possible options are as follows:

            - a single integer is interpreted as the number of doors to
            select (randomly, with equal probability)
            - a list of integers with `weighted=False` is interpeted as
            specific doors to pick, e.g. `[0, 2]` selects the doors at
            index 0 and index 2.
            - a list of integers with `weighted=True` is interpreted as
            probabilities/weights for selecting a single door.  The length
            of the weights can be either a) the same as the number of doors
            or b) less than the number of doors.  In the latter case, the
            number of weights must align with the number of selectable
            doors per row, based on the `exclude_...` arguments below.

        weighted : bool, optional
            Treat the first argument as weights (see docs above).
            The default is False.
        behavior : 'add', 'overwrite', or 'remove', optional
            How to treat the the new selections when applying them to the
            simulation. The default is 'overwrite'.
            - overwrite: new selections should simply replace the current target array.
            - add: any 1s in the new selections should be added to any 1s in
            the current target array (essentially an "or" operation)
            - remove: any 1s in the new selection should indicate places to remove 1s
            in the current array.
        exclude_picked : bool, optional
            Disallow selection of picked doors. The default is False.
        exclude_revealed : bool, optional
            Disallow selection of revealed doors. The default is False.
        exclude_cars : bool, optional
            Disallow selection of doors with cars. The default is False.
        exclude_unpicked : bool, optional
            Disallow selection of unpicked doors. The default is False.
        exclude_closed : bool, optional
            Disallow selection of closed doors. The default is False.
        exclude_carless : bool, optional
            Disallow selection of doors with goats. The default is False.
        allow_spoiled : bool, optional
            Do not throw an error of the game is spoiled. The default is False.
            Spoiled games are recorded in the `spoiled` attribute of the
            simulation.
        allow_redundant : bool, optional
            Do not throw an error if doors that are already set/unset are
            selected to be redundantly set/unset (respectively).
            The default is True.

        Raises
        ------
        ValueError
            `target` or `behavior` not in acceptable options, or problem
            interpreting `doors` as weights when `weights=True`.

        Returns
        -------
        None.

        '''

        if target not in ('picked', 'revealed', 'cars'):
            raise ValueError('Target must be "picked", "revealed", '
                             f'or "cars", not {target}.')
        if behavior not in ("overwrite", "add", "remove"):
            raise ValueError('`behavior` must be "overwrite", "add" or "remove"')

        self.target = target
        self.doors = doors
        self.weighted = weighted
        self.behavior = behavior
        self.exclude_picked = exclude_picked
        self.exclude_revealed = exclude_revealed
        self.exclude_cars = exclude_cars
        self.exclude_unpicked = exclude_unpicked
        self.exclude_closed = exclude_closed
        self.exclude_carless = exclude_carless
        self.allow_spoiled = allow_spoiled
        self.allow_redundant = allow_redundant

    def __call__(self, sim):
        # choice = self.doors

        allowed = ~sim.query_doors_or(picked=self.exclude_picked,
                                      revealed=self.exclude_revealed,
                                      cars=self.exclude_cars,
                                      not_picked=self.exclude_unpicked,
                                      not_revealed=self.exclude_closed,
                                      not_cars=self.exclude_carless)

        if self.doors == 1:
            new_array = one_per_row(sim.shape, allowed=allowed)
            n = 1
        elif isinstance(self.doors , int):
            new_array = n_per_row(sim.shape, n=self.doors, allowed=allowed)
            n = self.doors
        elif isinstance(self.doors, Iterable) and not self.weighted:
            new_array = np.zeros(sim.shape, dtype=int)
            new_array[:, self.doors] = 1
            n = len(self.doors)
        elif isinstance(self.doors, Iterable) and self.weighted:
            new_array = one_per_row_weighted(sim.shape, weights=self.doors,
                                             allowed=allowed)
            n = 1
        else:
            raise ValueError('Cannot interpret `doors` as an integer, '
                             'choice array, or weighted choice array. '
                             'Please see documentation.')

        sim._set_array(target=self.target,
                       new_array=new_array,
                       behavior=self.behavior,
                       n_per_row=n,
                       allow_spoiled=self.allow_spoiled,
                       allow_redundant=self.allow_redundant)

        return sim
