#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 20:37:53 2022

@author: earnestt1234
"""

from cargoat.steps.generic import GenericAction

class Close(GenericAction):
    def __init__(self, doors=1, weighted=False, exclude_current=True,
                 allow_spoiled=False, allow_redundant=True):
        super().__init__(target='revealed',
                         doors=doors,
                         weighted=weighted,
                         behavior='remove',
                         exclude_closed=exclude_current,
                         allow_redundant=allow_redundant,
                         allow_spoiled=allow_spoiled)

# class CloseDoor(MontyHallRule):
#     def __call__(self, sim):
#         closable = sim.revealed.astype(bool)
#         badrows = ~np.any(closable, axis=1)
#         if np.any(badrows):
#             msg = 'No open doors to close.'
#             bad_trials_raise(badrows, msg, BadClose)

#         to_close = one_per_row(sim.shape, allowed=closable, enforce_allowed=True)
#         newreveals = (closable - to_close).astype(int)
#         sim.set_revealed(newreveals, add=False)

# class CloseDoors(MontyHallRule):
#     def __init__(self, n):
#         self.n = n

#     def __call__(self, sim):
#         closable = sim.revealed.astype(bool)
#         badrows = ~np.any(closable, axis=1)
#         if np.any(badrows):
#             msg = f"Less than {self.n} open doors to close."
#             bad_trials_raise(badrows, msg, BadClose)

#         to_close = n_per_row(sim.shape, self.n,
#                               allowed=closable, enforce_allowed=True)
#         newreveals = (closable - to_close).astype(int)
#         sim.set_revealed(newreveals, add=False)

# class CloseSpecificDoors(MontyHallRule):
#     def __init__(self, doors):
#         if not isinstance(doors, Iterable):
#             doors = [doors]
#         self.doors = list(doors)

#     def __call__(self, sim):
#         check_closable = sim.revealed[:, self.doors]
#         badrows = np.any(check_closable != 1, axis=1)
#         if np.any(badrows):
#             msg = f'At least some doors at positions {self.doors} are not open.'
#             bad_trials_raise(badrows, msg, BadClose)

#         to_close = np.zeros(sim.shape, dtype=int)
#         to_close[:, self.doors] = 1
#         newreveals = (sim.revealed - to_close).astype(int)
#         sim.set_revealed(newreveals, add=False)
