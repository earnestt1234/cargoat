#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This was a proposed implementation making steps for different actions
more dependent on the same code.  It may be revisited in the future?
"""

from collections.abc import Iterable

import numpy as np

from cargoat.arrayops import (n_per_row,
                              one_per_row,
                              one_per_row_weighted)

# class _GenericActionSingleDoor():
#     def __init__(self, target, pre_func=None, allowed_func=None,
#                  behavior='overwrite', n_per_row=1,
#                  allow_spoiled=False, allow_redundant=True):
#         self.target = target
#         self.pre_func = pre_func
#         self.allowed_func = allowed_func
#         self.behavior = behavior
#         self.n_per_row = n_per_row
#         self.allow_spoiled = allow_spoiled
#         self.allow_redundant = allow_redundant

#     def __call__(self, sim):

#         if self.pre_func:
#             self.pre_func(sim)

#         if self.allowed_func is not None:
#             allowed = self.allowed_func(sim)
#         else:
#             allowed = np.ones(sim.shape, dtype=bool)

#         selections = one_per_row(sim.shape, allowed=allowed, dtype=int)
#         sim._set_array(target=self.target,
#                        new_array=selections,
#                        behavior=self.behavior,
#                        n_per_row=self.n_per_row,
#                        allow_spoiled=self.allow_spoiled,
#                        allow_redundant=self.allow_redundant)

class GenericAction:
    def __init__(self, target, doors=1, weighted=False, behavior='overwrite',
                 exclude_picked=False, exclude_revealed=False, exclude_cars=False,
                 exclude_unpicked=False,exclude_closed=False, exclude_carless=False,
                 allow_spoiled=False, allow_redundant=True):

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
