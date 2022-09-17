#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for the cargoat `MontyHallSimulation` class, which is used for
running a given Monty Hall experiment many times.
"""

import numpy as np

from cargoat.arrayops import get_index_success
from cargoat.errors import BadPick, BadReveal, bad_trials_raise, check_n_per_row

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

    # ---- Array setter functions

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

    def set_picks(self, picks, add=False, allow_spoiled=False, n_per_row=None):

        # check for correct number of picks
        if n_per_row is not None:
            check_n_per_row(picks, n=n_per_row, etype=BadPick,
                            emessage='Some trials have incorrect number of picks.')

        # check for valid picks
        valid = self.validate_picks(picks)
        invalid_rows = np.any(~valid, axis=1)
        if not allow_spoiled and np.any(~valid):
            trial, door = get_index_success(~valid)
            msg = ("Revealed doors were picked, e.g. "
                   f"trial {trial} door {door}.")
            bad_trials_raise(invalid_rows, msg, BadPick)

        # mark spoiled games (only based on invalid picks)
        self.spoiled[invalid_rows] = 1

        # update sim.picked
        if add:
            picks = np.logical_or(picks, self.picked).astype(int)
        self.picked = picks

    def set_new_picks(self, pick_array, behavior='overwrite',
                      strict_validate=False, n_per_row=None,
                      allow_spoiled=False):

        actionname = 'unpick' if behavior == 'remove' else 'pick'

         # strict validation
         #  - add/overwrite MUST satisfy n_per_row
         #  - remove must only target picked doors
         #    (and satisfy n_per_row unpicks)
        if behavior == 'remove':
            if strict_validate:
                valid = (self.picks - pick_array) >= 0
                invalid_rows = np.any(~valid, axis=1)
                if np.any(~valid, axis=1):
                    trial, door = get_index_success(~valid)
                    msg = ("Strict unpick tried on unpicked door, e.g. "
                           f"trial {trial} door {door}.")
                    bad_trials_raise(invalid_rows, msg, BadPick)

            # convert to an overwrite action of the difference in picks
            pick_array = self.picks - np.logical_and(pick_array, self.picks, dtype=int)
            behavior = 'overwrite'

        if behavior in ['add', 'overwrite']:
            if strict_validate and n_per_row is not None:
                emessage = f'Some trials have incorrect number of {actionname}s.'
                check_n_per_row(pick_array, n=n_per_row, etype=BadPick,
                                emessage=emessage)

        # now that new picks are finalized
        # check if they are valid in the game
        valid = self.validate_new_picks(pick_array)
        invalid_rows = np.any(~valid, axis=1)
        if not allow_spoiled and np.any(~valid):
            trial, door = get_index_success(~valid)
            msg = ("Revealed doors were picked, e.g. "
                   f"trial {trial} door {door}.")
            bad_trials_raise(invalid_rows, msg, BadPick)

        # mark spoiled games (only based on invalid picks)
        self.spoiled[invalid_rows] = 1

        # update sim.picked
        if behavior == 'add':
            pick_array = np.logical_or(pick_array, self.picked).astype(int)
        self.picked = pick_array

    def validate_picks(self, picks):
        return ~ np.logical_and(self.revealed, picks)

    def check_spoiling_picks(self, picks):
        return ~ np.logical_and(self.revealed, picks)

    # ---- Door revealing
    def set_revealed(self, reveals, add=True, allow_spoiled=False, n_per_row=None):

        # check for correct number of reveals
        if n_per_row is not None:
            check_n_per_row(reveals, n=n_per_row, etype=BadReveal,
                            emessage='Some trials have incorrect number of reveals.')

        # check for valid reveals
        valid = self.validate_reveals(reveals)
        invalid_rows = np.any(~valid, axis=1)
        if not allow_spoiled and np.any(~valid):
            trial, door = get_index_success(~valid)
            msg = ("Cars or picked doors were revealed, e.g. "
                   f"trial {trial} door {door}.")
            bad_trials_raise(invalid_rows, msg, BadReveal)

        # mark spoiled games (only based on invalid picks)
        self.spoiled[invalid_rows] = 1

        # update sim.revealed
        if add:
            reveals = np.logical_or(reveals, self.revealed).astype(int)
        self.revealed = reveals

    def validate_reveals(self, reveals):
        notokay = self.query_doors_or(cars=True, picked=True)
        return ~ np.logical_and(notokay, reveals)

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


