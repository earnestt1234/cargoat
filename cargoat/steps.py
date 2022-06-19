#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes for individual game rules applied to `MontyHallSim` objects.
"""

from collections.abc import Iterable
import pprint

import numpy as np

from cargoat.arrayops import one_per_row, n_per_row
from cargoat.errors import (BadReveal, bad_trials_raise)

# ---- Parent class
class MontyHallRule(object):
    def __repr__(self):
        name = self.__class__.__name__
        args = ', '.join(f'{arg}={val}' for arg, val in vars(self).items())
        return f'{name}({args})'

# ---- Initialization
class InitDoorsFixed(MontyHallRule):
    def __init__(self, placement=[0, 0, 1]):
        self.placement = np.array(placement).astype(int)

    def __call__(self, sim):
        shape = (sim.n, len(self.placement))
        sim.cars = np.tile(self.placement, (sim.n, 1))
        sim.picked = np.zeros(shape, dtype=int)
        sim.revealed = np.zeros(shape, dtype=int)
        sim.spoiled = np.zeros(sim.n, dtype=int)

class InitDoorsRandom(MontyHallRule):
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

# ---- Picking Doors
class PickDoor(MontyHallRule):
    def __init__(self, exclude_current=True, exclude_revealed=True, add=False,
                 allow_spoiled=False):
        self.exclude_current = exclude_current
        self.exclude_revealed = exclude_revealed
        self.allow_spoiled = allow_spoiled
        self.add = add

    def __call__(self, sim):
        pickable = ~sim.query_doors_or(picked=self.exclude_current,
                                       revealed=self.exclude_revealed)
        newpicks = one_per_row(sim.shape, allowed=pickable)
        sim.set_picks(newpicks, add=self.add, n_per_row=1, allow_spoiled=self.allow_spoiled)

class PickDoors(MontyHallRule):
    def __init__(self, n, exclude_current=True, exclude_revealed=True, add=False,
                 allow_spoiled=False):
        self.n = n
        self.exclude_current = exclude_current
        self.exclude_revealed = exclude_revealed
        self.add = add
        self.allow_spoiled = allow_spoiled

    def __call__(self, sim):
        pickable = ~sim.query_doors_or(picked=self.exclude_current,
                                       revealed=self.exclude_revealed)
        newpicks = n_per_row(sim.shape, n=self.n, allowed=pickable)
        sim.set_picks(newpicks, add=self.add, n_per_row=self.n, allow_spoiled=self.allow_spoiled)

class PickDoorWeighted(MontyHallRule):
    def __init__(self, weights, exclude_revealed=True, exclude_current=True,
                 allow_spoiled=False, add=False):
        self.weights = weights
        self.exclude_revealed = exclude_revealed
        self.exclude_current = exclude_current
        self.allow_spoiled = allow_spoiled
        self.add = add

    def __call__(self, sim):
        w = self.weights
        n, d = sim.shape

        # init empty weights
        wmat = np.full(sim.shape, np.nan)

        # unweight if desired
        if self.exclude_revealed:
            wmat[sim.revealed.astype(bool)] = 0
        if self.exclude_current:
            wmat[sim.picked.astype(bool)] = 0

        # fill in provided weights
        if isinstance(w, Iterable) and len(w) == d:
            wmat = np.where(np.isnan(wmat),
                            np.tile(w, (n, 1)),
                            wmat)
        elif isinstance(w, Iterable):
            lw = len(w)
            spots = np.sum(np.isnan(wmat), axis=1)
            if ~ np.all(spots == lw):
                badtrials = spots != lw
                msg = 'Weights do not match number of pickable doors.'
                bad_trials_raise(badtrials, msg, ValueError)
            wmat[np.isnan(wmat)] = np.tile(w, n)

        # convert to probabilities
        pmat = wmat / wmat.sum(axis=1)[:, np.newaxis]

        cum_p = np.cumsum(pmat, axis=1)
        draws = np.random.rand(n, 1)
        lt = (cum_p < draws)
        to_pick = lt.sum(axis=1)

        picks = np.zeros(sim.shape, dtype=int)
        picks[sim.idx, to_pick] = 1
        sim.set_picks(picks, allow_spoiled=self.allow_spoiled, add=self.add)

class PickSpecificDoors(MontyHallRule):
    def __init__(self, doors, add=False, allow_spoiled=False):
        if not isinstance(doors, Iterable):
            doors = [doors]
        self.doors = list(doors)
        self.add = add
        self.allow_spoiled = allow_spoiled

    def __call__(self, sim):
        newpicks = np.zeros(sim.shape, dtype=int)
        newpicks[:, self.doors] = 1
        sim.set_picks(newpicks, add=self.add, allow_spoiled=self.allow_spoiled)

class Stay(MontyHallRule):
    def __call__(self, sim):
        pass

class Switch(MontyHallRule):
    def __call__(self, sim):
        PickDoor()(sim)

# ---- Revealing Doors
class RevealDoor(MontyHallRule):
    def __init__(self, exclude_current=True, exclude_cars=True,
                 exclude_picked=True, allow_spoiled=False):
        self.exclude_current = exclude_current
        self.exclude_cars = exclude_cars
        self.exclude_picked=exclude_picked
        self.allow_spoiled = allow_spoiled

    def __call__(self, sim):
        revealable = ~sim.query_doors_or(cars=self.exclude_cars,
                                         revealed=self.exclude_current,
                                         picked=self.exclude_picked)
        newreveals = one_per_row(sim.shape, allowed=revealable)
        sim.set_revealed(newreveals, add=True, n_per_row=1, allow_spoiled=self.allow_spoiled)

class RevealDoors(MontyHallRule):
    def __init__(self, n, exclude_current=True, exclude_cars=True,
                 exclude_picked=True, allow_spoiled=False):
        self.n = n
        self.exclude_current = exclude_current
        self.exclude_cars = exclude_cars
        self.exclude_picked=exclude_picked
        self.allow_spoiled = allow_spoiled

    def __call__(self, sim):
        revealable = ~sim.query_doors_or(cars=self.exclude_cars,
                                         revealed=self.exclude_current,
                                         picked=self.exclude_picked)
        newreveals = n_per_row(sim.shape, n=self.n, allowed=revealable)
        sim.set_revealed(newreveals, add=True, n_per_row=self.n, allow_spoiled=self.allow_spoiled)

class RevealGoat(MontyHallRule):
    def __call__(self, sim):
        revealable = sim.revealable_doors()
        badrows = ~np.any(revealable, axis=1)
        if np.any(badrows):
            msg = "No goats to reveal."
            bad_trials_raise(badrows, msg, BadReveal)

        weights = np.random.rand(*sim.shape) * revealable
        to_reveal = weights.argmax(1)
        sim.revealed[sim.idx, to_reveal] = 1

# ---- Other
class Finish(MontyHallRule):
    def __call__(self, sim):
        pprint.pprint(sim.get_results(), sort_dicts=False)