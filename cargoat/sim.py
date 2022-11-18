#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for the cargoat `MontyHallSimulation` class, which is used for
running a given Monty Hall experiment many times.
"""

import numpy as np

from cargoat.arrayops import get_index_success
from cargoat.errors import (
    BadPick,
    BadReveal,
    bad_trials_raise,
    check_n_per_row,
    check_redundancy_for_setting,
    get_errortype_from_behavior
    )

class MontyHallSim:
    def __init__(self, n):
        self.n = n

        self.cars = np.empty(0)
        self.picked = np.empty(0)
        self.revealed = np.empty(0)
        self.spoiled = np.empty(0)

    # ---- Class methods

    @classmethod
    def from_arrays(cls, picked=None, revealed=None, cars=None,
                    spoiled=None, default=0, copy=True):

        mainarrays = (cars, picked, revealed)

        if all([i is None for i in mainarrays]):
            raise ValueError('Must provide at least one of cars, '
                             'picked, or revealed.')

        base = [a for a in mainarrays if a is not None][0]
        shape = base.shape

        if picked is None:
            picked = np.full(shape, default)
        if revealed is None:
            revealed = np.full(shape, default)
        if cars is None:
            cars = np.full(shape, default)

        shape_set = set(i.shape for i in (cars, picked, revealed))

        if len(shape_set) != 1:
            raise ValueError('Detected different array shapes for '
                             'picked, revealed, and cars.')

        n, doors = shape
        if spoiled is None:
            spoiled = np.zeros(n, dtype=int)
        if len(spoiled) != n:
            raise ValueError('spoiled array does not match')

        copyfun = (lambda x: x.copy()) if copy else (lambda x: x)

        out = cls(n)
        out.cars = copyfun(cars)
        out.picked = copyfun(picked)
        out.revealed = copyfun(revealed)
        out.spoiled = copyfun(spoiled)

        return out

    # ---- Properties
    @property
    def idx(self):
        return np.arange(self.n)

    @property
    def shape(self):
        return self.cars.shape

    # ---- Status of the sim
    def pickable_doors(self, exclude_current=True):
        return ~self.query_doors_or(picked=exclude_current, revealed=True)

    def query_doors_or(self, cars=False, picked=False, revealed=False,
                       not_cars=False, not_picked=False, not_revealed=False):
        c = int(cars)
        p = int(picked)
        r = int(revealed)
        notc = int(not_cars)
        notp = int(not_picked)
        notr = int(not_revealed)

        out = np.logical_or.reduce([
            c * self.cars,
            p * self.picked,
            r * self.revealed,
            notc * (1 - self.cars),
            notp * (1 - self.picked),
            notr * (1 - self.revealed)
            ])
        return out

    def revealable_doors(self):
        return ~self.query_doors_or(cars=True, picked=True, revealed=True)

    # ---- Generic setter functions

    def _get_spoiling_func(self, target):
        if target == 'picked':
            return self._check_spoiling_picks

        elif target == 'revealed':
            return self._check_spoiling_reveals

        else:
            raise NotImplementedError

    def _set_array(self, target, new_array,
                   behavior='overwrite', n_per_row=None, allow_spoiled=False,
                   allow_redundant=True):

        old_array = getattr(self, target)
        check_spoiling = self._get_spoiling_func(target)
        etype = get_errortype_from_behavior(target=target, behavior=behavior)

        # apply checks if requested
        if n_per_row is not None:
            check_n_per_row(a=new_array, n=n_per_row, etype=etype)

        if not allow_redundant:
            check_redundancy_for_setting(old_array=old_array, new_array=new_array,
                                         behavior=behavior, etype=etype)

        # then check for valid action
        kosher = check_spoiling(new_array, behavior=behavior, allow_spoiled=allow_spoiled)

        # mark spoiled games (only based on invalid picks)
        spoiling_rows = np.any(~kosher, axis=1)
        self.spoiled[spoiling_rows] = 1

        # update sim.picked
        if behavior == 'add':
            new_array = np.logical_or(new_array, old_array).astype(int)
        elif behavior == 'remove':
            new_array = old_array - np.logical_and(new_array, old_array, dtype=int)
            new_array[new_array < 0] = 0

        setattr(self, target, new_array)

    # ---- Pick setting

    def _check_spoiling_picks(self, picks, behavior, allow_spoiled=True):
        if behavior in ['add', 'overwrite']:
            valid =  ~ np.logical_and(self.revealed, picks)
        elif behavior == 'remove':
            valid = np.full(True, self.shape)

        if not allow_spoiled and np.any(~valid):
            invalid_rows = np.any(~valid, axis=1)
            trial, door = get_index_success(~valid)
            msg = ("Revealed doors were picked, e.g. "
                   f"trial {trial} door {door}.")
            bad_trials_raise(invalid_rows, msg, BadPick)

        return valid

    # ---- Door revealing

    def _check_spoiling_reveals(self, reveals, behavior, allow_spoiled=True):
        offlimits = self.query_doors_or(cars=True, picked=True)
        if behavior in ['add', 'overwrite']:
            valid =  ~np.logical_and(offlimits, reveals)
        elif behavior == 'remove':
            valid = np.full(self.shape, True)

        if not allow_spoiled and np.any(~valid):
            invalid_rows = np.any(~valid, axis=1)
            trial, door = get_index_success(~valid)
            msg = ("Cars or picked doors were revealed, e.g. "
                   f"trial {trial} door {door}.")
            bad_trials_raise(invalid_rows, msg, BadReveal)

        return valid

    # ---- Other Helpers
    def apply_func(self, func, inplace=False, cars=True, picked=True, revealed=True):
        apply_to = [x for i, x in enumerate(['cars', 'picked', 'revealed'])
                    if [cars, picked, revealed][i]]
        for attr in apply_to:
            a = getattr(self, attr)
            if inplace:
                func(a)
            else:
                setattr(self, attr, func(a))

    # ---- Results
    def get_results(self):
        wins = np.sum(np.any(self.picked * self.cars, axis=1))
        losses = self.n - wins
        percent_wins = (wins / self.n) * 100
        percent_losses = (losses / self.n) * 100
        results = {
            'trials': self.n,
            'wins': wins,
            'losses': losses,
            'percent_wins': percent_wins,
            'percent_losses': percent_losses
            }

        return results


