#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 20:37:53 2022

@author: earnestt1234
"""

from cargoat.steps.generic import GenericAction

class Reveal(GenericAction):
    def __init__(self, doors=1, weighted=False, exclude_current=True,
                 exclude_cars=True, exclude_picked=True,
                 allow_spoiled=False, allow_redundant=True):
        super().__init__(target='revealed',
                         doors=doors,
                         weighted=weighted,
                         behavior='add',
                         exclude_picked=exclude_picked,
                         exclude_revealed=exclude_current,
                         exclude_cars=exclude_cars,
                         allow_redundant=allow_redundant,
                         allow_spoiled=allow_spoiled)

# class RevealDoor(MontyHallRule):
#     def __init__(self, exclude_current=True, exclude_cars=True,
#                   exclude_picked=True, allow_spoiled=False):
#         self.exclude_current = exclude_current
#         self.exclude_cars = exclude_cars
#         self.exclude_picked=exclude_picked
#         self.allow_spoiled = allow_spoiled

#     def __call__(self, sim):
#         revealable = ~sim.query_doors_or(cars=self.exclude_cars,
#                                           revealed=self.exclude_current,
#                                           picked=self.exclude_picked)
#         newreveals = one_per_row(sim.shape, allowed=revealable)
#         sim._set_array(target='revealed',
#                        new_array=newreveals,
#                        behavior='add',
#                        n_per_row=1,
#                        allow_spoiled=self.allow_spoiled,
#                        allow_redundant=True)

# class RevealDoors(MontyHallRule):
#     def __init__(self, n, exclude_current=True, exclude_cars=True,
#                   exclude_picked=True, allow_spoiled=False):
#         self.n = n
#         self.exclude_current = exclude_current
#         self.exclude_cars = exclude_cars
#         self.exclude_picked=exclude_picked
#         self.allow_spoiled = allow_spoiled

#     def __call__(self, sim):
#         revealable = ~sim.query_doors_or(cars=self.exclude_cars,
#                                           revealed=self.exclude_current,
#                                           picked=self.exclude_picked)
#         newreveals = n_per_row(sim.shape, n=self.n, allowed=revealable)
#         sim._set_array(target='revealed',
#                        new_array=newreveals,
#                        behavior='add',
#                        n_per_row=self.n,
#                        allow_spoiled=self.allow_spoiled,
#                        allow_redundant=True)

# class RevealSpecificDoors(MontyHallRule):
#     def __init__(self, doors, allow_spoiled=False, allow_redundant=True):
#         if not isinstance(doors, Iterable):
#             doors = [doors]
#         self.doors = list(doors)
#         self.allow_spoiled = allow_spoiled
#         self.allow_redundant = allow_redundant

#     def __call__(self, sim):
#         newreveals = np.zeros(sim.shape, dtype=int)
#         newreveals[:, self.doors] = 1
#         sim._set_array(target='revealed',
#                        new_array=newreveals,
#                        behavior='add',
#                        n_per_row=len(self.doors),
#                        allow_spoiled=self.allow_spoiled,
#                        allow_redundant=self.allow_redundant)

# class RevealDoorWeighted(MontyHallRule):
#     def __init__(self, weights, exclude_current=True, exclude_cars=True,
#                   exclude_picked=True, allow_spoiled=False):
#         self.weights = weights
#         self.exclude_current = exclude_current
#         self.exclude_cars = exclude_cars
#         self.exclude_picked=exclude_picked
#         self.allow_spoiled = allow_spoiled

#     def __call__(self, sim):

#         allowed = np.ones(sim.shape, dtype=bool)
#         if self.exclude_current:
#             allowed[sim.revealed.astype(bool)] = 0
#         if self.exclude_cars:
#             allowed[sim.cars.astype(bool)] = 0
#         if self.exclude_picked:
#             allowed[sim.picked.astype(bool)] = 0

#         reveals = one_per_row_weighted(sim.shape, weights=self.weights, allowed=allowed)
#         sim._set_array(target='revealed',
#                        new_array=reveals,
#                        behavior='add',
#                        n_per_row=1,
#                        allow_spoiled=self.allow_spoiled,
#                        allow_redundant=True)

# class RevealGoat(MontyHallRule):
#     def __call__(self, sim):
#         revealable = sim.revealable_doors()
#         badrows = ~np.any(revealable, axis=1)
#         if np.any(badrows):
#             msg = "No goats to reveal."
#             bad_trials_raise(badrows, msg, BadReveal)

#         newreveals = one_per_row(sim.shape, allowed=revealable)
#         sim._set_array(target='revealed',
#                        new_array=newreveals,
#                        behavior='add',
#                        n_per_row=1,
#                        allow_spoiled=False,
#                        allow_redundant=False)

# class RevealGoats(MontyHallRule):
#     def __init__(self, n):
#         self.n = n

#     def __call__(self, sim):
#         revealable = sim.revealable_doors()
#         badrows = revealable.sum(axis=1) < self.n
#         if np.any(badrows):
#             msg = f"Less than {self.n} goats to reveal."
#             bad_trials_raise(badrows, msg, BadReveal)

#         newreveals = n_per_row(sim.shape, n=self.n, allowed=revealable)
#         sim._set_array(target='revealed',
#                        new_array=newreveals,
#                        behavior='add',
#                        n_per_row=self.n,
#                        allow_spoiled=False,
#                        allow_redundant=False)
