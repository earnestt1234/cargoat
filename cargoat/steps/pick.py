#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 08:52:01 2022

@author: earnestt1234
"""

from cargoat.steps.generic import GenericAction

class Pick(GenericAction):
    def __init__(self, doors=1, weighted=False, exclude_current=True,
                 exclude_revealed=True, add=False, allow_spoiled=False,
                 allow_redundant=True):
        behavior = 'add' if add else 'overwrite'
        super().__init__(target='picked',
                         doors=doors,
                         weighted=weighted,
                         behavior=behavior,
                         exclude_picked=exclude_current,
                         exclude_revealed=exclude_revealed,
                         allow_redundant=allow_redundant,
                         allow_spoiled=allow_spoiled)

# class Pick:
#     def __init__(self, doors=1, weighted=False, exclude_current=True,
#                  exclude_revealed=True, add=False, allow_spoiled=False,
#                  allow_redundant=True):
#         self.doors = doors
#         self.weighted = weighted
#         self.exclude_current = exclude_current
#         self.exclude_revealed = exclude_revealed
#         self.add = add
#         self.allow_spoiled = allow_spoiled
#         self.allow_redundant = allow_redundant

#     def __call__(self, sim):
#         # choice = self.doors
#         allowed = ~sim.query_doors_or(picked=self.exclude_current,
#                                       revealed=self.exclude_revealed)
#         if self.doors == 1:
#             new_array = one_per_row(sim.shape, allowed=allowed)
#             n = 1
#         elif isinstance(self.doors , int):
#             new_array = n_per_row(sim.shape, n=self.doors, allowed=allowed)
#             n = self.doors
#         elif isinstance(self.doors, Iterable) and not self.weighted:
#             new_array = np.zeros(sim.shape, dtype=int)
#             new_array[:, self.doors] = 1
#             n = len(self.doors)
#         elif isinstance(self.doors, Iterable) and self.weighted:
#             new_array = one_per_row_weighted(sim.shape, weights=self.doors,
#                                              allowed=allowed)
#             n = 1
#         else:
#             raise ValueError('Cannot interpret `doors` as an integer, '
#                              'choice array, or weighted choice array. '
#                              'Please see documentation.')

#         behavior = 'add' if self.add else 'overwrite'
#         sim._set_array(target='picked',
#                        new_array=new_array,
#                        behavior=behavior,
#                        n_per_row=n,
#                        allow_spoiled=self.allow_spoiled,
#                        allow_redundant=self.allow_redundant)

# class PickDoor(MontyHallRule):
#     def __init__(self, exclude_current=True, exclude_revealed=True, add=False,
#                  allow_spoiled=False):
#         self.exclude_current = exclude_current
#         self.exclude_revealed = exclude_revealed
#         self.allow_spoiled = allow_spoiled
#         self.add = add

#     def __call__(self, sim):
#         pickable = ~sim.query_doors_or(picked=self.exclude_current,
#                                        revealed=self.exclude_revealed)
#         newpicks = one_per_row(sim.shape, allowed=pickable)
#         behavior = 'add' if self.add else 'overwrite'
#         sim._set_array(target='picked',
#                        new_array=newpicks,
#                        behavior=behavior,
#                        n_per_row=1,
#                        allow_spoiled=self.allow_spoiled,
#                        allow_redundant=True)

# class PickDoors(MontyHallRule):
#     def __init__(self, n, exclude_current=True, exclude_revealed=True, add=False,
#                   allow_spoiled=False):
#         self.n = n
#         self.exclude_current = exclude_current
#         self.exclude_revealed = exclude_revealed
#         self.add = add
#         self.allow_spoiled = allow_spoiled

#     def __call__(self, sim):
#         pickable = ~sim.query_doors_or(picked=self.exclude_current,
#                                        revealed=self.exclude_revealed)
#         newpicks = n_per_row(sim.shape, n=self.n, allowed=pickable)
#         behavior = 'add' if self.add else 'overwrite'
#         sim._set_array(target='picked',
#                        new_array=newpicks,
#                        behavior=behavior,
#                        n_per_row=self.n,
#                        allow_spoiled=self.allow_spoiled,
#                        allow_redundant=True)

# class PickDoorWeighted(MontyHallRule):
#     def __init__(self, weights, exclude_revealed=True, exclude_current=True,
#                   allow_spoiled=False, add=False):
#         self.weights = weights
#         self.exclude_revealed = exclude_revealed
#         self.exclude_current = exclude_current
#         self.allow_spoiled = allow_spoiled
#         self.add = add

#     def __call__(self, sim):

#         allowed = np.ones(sim.shape, dtype=bool)
#         if self.exclude_revealed:
#             allowed[sim.revealed.astype(bool)] = 0
#         if self.exclude_current:
#             allowed[sim.picked.astype(bool)] = 0

#         picks = one_per_row_weighted(sim.shape, weights=self.weights,
#                                      allowed=allowed)
#         behavior = 'add' if self.add else 'overwrite'
#         sim._set_array(target='picked',
#                        new_array=picks,
#                        behavior=behavior,
#                        n_per_row=self.n,
#                        allow_spoiled=self.allow_spoiled,
#                        allow_redundant=True)

# class PickSpecificDoors(MontyHallRule):
#     def __init__(self, doors, add=False, allow_spoiled=False, allow_redundant=True):
#         if not isinstance(doors, Iterable):
#             doors = [doors]
#         self.doors = list(doors)
#         self.add = add
#         self.allow_spoiled = allow_spoiled
#         self.allow_redundant = allow_redundant

#     def __call__(self, sim):
#         newpicks = np.zeros(sim.shape, dtype=int)
#         newpicks[:, self.doors] = 1
#         behavior = 'add' if self.add else 'overwrite'
#         sim._set_array(target='picked',
#                        new_array=newpicks,
#                        behavior=behavior,
#                        n_per_row=len(self.doors),
#                        allow_spoiled=self.allow_spoiled,
#                        allow_redundant=self.allow_redundant)
