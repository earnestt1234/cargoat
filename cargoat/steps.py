#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes for individual game rules applied to `MontyHallSim` objects.
"""

from collections.abc import Iterable
from numbers import Number
import pprint

import numpy as np

from cargoat.errors import (BadPick, BadReveal)

# ---- Parent class
class MontyHallRule(object):
    def __repr__(self):
        name = self.__class__.__name__
        args = ', '.join(f'{arg}={val}' for arg, val in vars(self).items())
        return f'{name}({args})'

    def bad_trials_raise(self, badrows, msg, errortype):
        idx = np.arange(len(badrows))[badrows]
        n = len(idx)
        raise errortype(f"{msg} Found for {n} trial(s):\n{idx}")

# ---- Initialization
class InitDoorsRandom(MontyHallRule):
    def __init__(self, cars=1, goats=2):
        self.cars = cars
        self.goats = goats

    def __call__(self, sim):
        shape = (sim.n, self.cars + self.goats)
        sim.cars = np.zeros(shape).astype(int)
        sim.picked = np.zeros(shape).astype(int)
        sim.revealed = np.zeros(shape).astype(int)

        p = np.random.rand(shape[0], shape[1]).argsort(1)
        sim.cars[p < self.cars] = 1

# ---- Picking Doors
class PickDoor(MontyHallRule):
    def __call__(self, sim):
        pickable = sim.pickable_doors()
        badrows = ~np.any(pickable, axis=1)
        if np.any(badrows):
            msg = "No pickable doors."
            self.bad_trials_raise(badrows, msg, BadPick)

        newpicks = np.zeros(sim.shape)
        weights = np.random.rand(*sim.shape) * pickable
        to_pick = weights.argmax(1)
        newpicks[sim.idx, to_pick] = 1
        sim.picked = newpicks.astype(int)

class PickDoorWeighted(MontyHallRule):
    def __init__(self, weights):
        if self.weights_type_okay(weights):
            self.weights = weights
        else:
            raise TypeError("weights must be None, a number, or an "
                            f"iterable of numbers, not {type(weights)}")

    def __call__(self, sim):
        w = self.weights
        if isinstance(w, Iterable) and len(w) == sim.shape[1]:
            pass
        else:
            raise NotImplementedError("Only implemented weights of same "
                                      "length as number of doors.")

    def weights_type_okay(self, weights):
        ok1 = weights is None
        ok2 = isinstance(weights, Number)

        isiterable = isinstance(weights, Iterable)
        if isiterable:
            nonnull = len(weights) >= 1
            numbers = all(isinstance(i, Number) for i in weights)
            ok3 = nonnull and numbers

        return any([ok1, ok2, ok3])

class Stay(MontyHallRule):
    def __call__(self, sim):
        pass

class Switch(MontyHallRule):
    def __call__(self, sim):
        PickDoor()(sim)

# class PickDoorN(MontyHallRule):
#     def __init__(self, door):
#         self.door = door

#     def __call__(self, sim):
#         prior = sim.picked.copy()
#         sim.picked[sim.idx, self.door] = 1

#         badpicks = np.logical_and(sim.picked - prior, sim.revealed)
#         if np.any(badpicks):
#             msg = "A revealed door was picked."
#             self.bad_trials_raise(np.any(badpicks, axis=1), msg, BadPick)

# ---- Revealing Doors
class RevealGoat(MontyHallRule):
    def __call__(self, sim):
        revealable = sim.revealable_doors()
        badrows = ~np.any(revealable, axis=1)
        if np.any(badrows):
            msg = "No goats to reveal."
            self.bad_trials_raise(badrows, msg, BadReveal)

        weights = np.random.rand(*sim.shape) * revealable
        to_reveal = weights.argmax(1)
        sim.revealed[sim.idx, to_reveal] = 1

# ---- Other
class Finish(MontyHallRule):
    def __call__(self, sim):
        pprint.pprint(sim.get_results(), sort_dicts=False)