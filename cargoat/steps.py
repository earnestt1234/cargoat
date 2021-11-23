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
    def __init__(self, weights, unweight_revealed=True, unweight_picked=True):
        self.weights = weights
        self.unweight_revealed = unweight_revealed
        self.unweight_picked = unweight_picked

    def __call__(self, sim):
        w = self.weights
        n, d = sim.shape

        # init empty weights
        wmat = np.full(sim.shape, np.nan)

        # unweight if desired
        if self.unweight_revealed:
            wmat[sim.revealed] = 0
        if self.unweight_picked:
            wmat[sim.picked] = 0

        # fill in provided weights
        if isinstance(w, Iterable) and len(w) == d:
            wmat = np.where(np.isnan(wmat),
                            np.tile(w, (n, 1)),
                            wmat)
        elif isinstance(w, Iterable):
            lw = len(w)

            pass

        # convert to probabilities
        pmat = wmat / wmat.sum(axis=1)[:, np.newaxis]

        cum_p = np.cumsum(pmat, axis=1)
        draws = np.random.rand(n, 1)
        lt = (cum_p < draws)
        to_pick = lt.sum(axis=1)

        picks = np.zeros(sim.shape)
        picks[sim.idx, to_pick] = 1

        # verify revealed doors aren't chosen
        valid = sim.validate_picks(picks)
        if np.any(~valid):
            badrows = np.any(~valid, axis=1)
            msg = "Revealed doors were picked."
            self.bad_trials_raise(badrows, msg, BadPick)

        # set the new picks
        sim.picked = picks

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