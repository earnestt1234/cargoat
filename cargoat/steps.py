#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes for individual game rules applied to `MontyHallSim` objects.
"""

from collections.abc import Iterable
import pprint

import numpy as np

from cargoat.arrayops import (one_per_row,
                              one_per_row_weighted,
                              n_per_row)
from cargoat.errors import (BadClose, BadReveal, bad_trials_raise)

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

        allowed = np.ones(sim.shape, dtype=bool)
        if self.exclude_revealed:
            allowed[sim.revealed.astype(bool)] = 0
        if self.exclude_current:
            allowed[sim.picked.astype(bool)] = 0

        picks = one_per_row_weighted(sim.shape, weights=self.weights,
                                     allowed=allowed)
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

class RevealSpecificDoors(MontyHallRule):
    def __init__(self, doors, allow_spoiled=False):
        if not isinstance(doors, Iterable):
            doors = [doors]
        self.doors = list(doors)
        self.allow_spoiled = allow_spoiled

    def __call__(self, sim):
        newreveals = np.zeros(sim.shape, dtype=int)
        newreveals[:, self.doors] = 1
        sim.set_revealed(newreveals, allow_spoiled=self.allow_spoiled)

class RevealDoorWeighted(MontyHallRule):
    def __init__(self, weights, exclude_current=True, exclude_cars=True,
                 exclude_picked=True, allow_spoiled=False):
        self.weights = weights
        self.exclude_current = exclude_current
        self.exclude_cars = exclude_cars
        self.exclude_picked=exclude_picked
        self.allow_spoiled = allow_spoiled

    def __call__(self, sim):

        allowed = np.ones(sim.shape, dtype=bool)
        if self.exclude_current:
            allowed[sim.revealed.astype(bool)] = 0
        if self.exclude_cars:
            allowed[sim.cars.astype(bool)] = 0
        if self.exclude_picked:
            allowed[sim.picked.astype(bool)] = 0

        reveals = one_per_row_weighted(sim.shape, weights=self.weights, allowed=allowed)
        sim.set_revealed(reveals, allow_spoiled=self.allow_spoiled)

class RevealGoat(MontyHallRule):
    def __call__(self, sim):
        revealable = sim.revealable_doors()
        badrows = ~np.any(revealable, axis=1)
        if np.any(badrows):
            msg = "No goats to reveal."
            bad_trials_raise(badrows, msg, BadReveal)

        newreveals = one_per_row(sim.shape, allowed=revealable)
        sim.set_revealed(newreveals, add=True, n_per_row=1)

class RevealGoats(MontyHallRule):
    def __init__(self, n):
        self.n = n

    def __call__(self, sim):
        revealable = sim.revealable_doors()
        badrows = revealable.sum(axis=1) < self.n
        if np.any(badrows):
            msg = f"Less than {self.n} goats to reveal."
            bad_trials_raise(badrows, msg, BadReveal)

        newreveals = n_per_row(sim.shape, n=self.n, allowed=revealable)
        sim.set_revealed(newreveals, add=True, n_per_row=self.n)

# ---- Closing Doors

class CloseDoor(MontyHallRule):
    def __call__(self, sim):
        closable = sim.revealed.astype(bool)
        badrows = ~np.any(closable, axis=1)
        if np.any(badrows):
            msg = 'No open doors to close.'
            bad_trials_raise(badrows, msg, BadClose)

        to_close = one_per_row(sim.shape, allowed=closable, enforce_allowed=True)
        newreveals = (closable - to_close).astype(int)
        sim.set_revealed(newreveals, add=False)

class CloseDoors(MontyHallRule):
    def __init__(self, n):
        self.n = n

    def __call__(self, sim):
        closable = sim.revealed.astype(bool)
        badrows = ~np.any(closable, axis=1)
        if np.any(badrows):
            msg = f"Less than {self.n} open doors to close."
            bad_trials_raise(badrows, msg, BadClose)

        to_close = n_per_row(sim.shape, self.n,
                             allowed=closable, enforce_allowed=True)
        newreveals = (closable - to_close).astype(int)
        sim.set_revealed(newreveals, add=False)

class CloseSpecificDoors(MontyHallRule):
    def __init__(self, doors):
        if not isinstance(doors, Iterable):
            doors = [doors]
        self.doors = list(doors)

    def __call__(self, sim):
        check_closable = sim.revealed[:, self.doors]
        badrows = np.any(check_closable != 1, axis=1)
        if np.any(badrows):
            msg = f'At least some doors at positions {self.doors} are not open.'
            bad_trials_raise(badrows, msg, BadClose)

        to_close = np.zeros(sim.shape, dtype=int)
        to_close[:, self.doors] = 1
        newreveals = (sim.revealed - to_close).astype(int)
        sim.set_revealed(newreveals, add=False)

# ---- Changing Doors

class AddDoors(MontyHallRule):
    def __init__(self, positions):
        self.positions = positions

    def __call__(self, sim):
        for attr in ['cars', 'picked', 'revealed']:
            a = getattr(sim, attr)
            newa = np.insert(arr=a, obj=self.positions, values=0, axis=1)
            setattr(sim, attr, newa)

class RemoveDoors(MontyHallRule):
    def __init__(self, positions):
        self.positions = positions

    def __call__(self, sim):
        for attr in ['cars', 'picked', 'revealed']:
            a = getattr(sim, attr)
            newa = np.delete(arr=a, obj=self.positions, axis=1)
            setattr(sim, attr, newa)

# ---- Other
class Finish(MontyHallRule):
    def __call__(self, sim):
        pprint.pprint(sim.get_results(), sort_dicts=False)