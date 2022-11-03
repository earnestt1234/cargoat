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

    def _get_setter_func(self, key):

        if key == 'picks':
            return self.set_new_picks
        elif key == 'revealed':
            return self.set_revealed
        elif key == 'cars':
            raise NotImplementedError
        else:
            raise ValueError("Key must be one of 'cars', 'picked', or 'revealed' "
                             f"not '{key}'.")

    def _get_validator_func(self, target):
        if target == 'picked':
            return self._validate_picks

        elif target == 'revealed':
            return self._validate_reveals

        else:
            raise NotImplementedError

    def _set_array(self, target, new_array,
                   behavior='overwrite', n_per_row=None, allow_spoiled=False,
                   allow_redundant=True):

        old_array = getattr(self, target)
        validator_func = self._get_validator_func(target)
        etype = get_errortype_from_behavior(target=target, behavior=behavior)

        # apply checks if requested
        if n_per_row is not None:
            check_n_per_row(a=new_array, n=n_per_row, etype=etype)

        if not allow_redundant:
            check_redundancy_for_setting(old_array=old_array, new_array=new_array,
                                         behavior=behavior, etype=etype)

        # then check for valid action
        valid = validator_func(new_array, behavior=behavior, allow_spoiled=allow_spoiled)

        # mark spoiled games (only based on invalid picks)
        invalid_rows = np.any(~valid, axis=1)
        self.spoiled[invalid_rows] = 1

        # update sim.picked
        if behavior == 'add':
            new_array = np.logical_or(new_array, old_array).astype(int)
        elif behavior == 'remove':
            new_array = old_array - np.logical_and(new_array, old_array, dtype=int)
            new_array[new_array < 0] = 0

        setattr(self, target, new_array)

    # ---- Pick setting

    def _validate_picks(self, picks, behavior, allow_spoiled=True):
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

    def _validate_reveals(self, reveals, behavior, allow_spoiled=True):
        offlimits = self.query_doors_or(cars=True, picked=True)
        if behavior in ['add', 'overwrite']:
            valid =  ~np.logical_and(offlimits, reveals)
        elif behavior == 'remove':
            valid = np.full(True, self.shape)

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


