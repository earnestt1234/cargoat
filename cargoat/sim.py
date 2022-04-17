#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for the cargoat `MontyHallSimulation` class, which is used for
running a given Monty Hall experiment many times.
"""

import numpy as np

from .errors import BadPick, BadReveal

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

    def pickable_doors(self, exclude_current=True):
        return ~self.query_doors_or(picked=exclude_current, revealed=True)

    def revealable_doors(self):
        return ~self.query_doors_or(cars=True, picked=True, revealed=True)

    # ---- Helpers for generating picks/reveals/cars

    def generate_rowwise_selections(self, n=1, array_allowed=None):

        if array_allowed is None:
            array_allowed = np.ones(self.shape, dtype=int)

        output = np.zeros(self.shape, dtype=int)
        weights = np.random.rand(*self.shape) * array_allowed
        indices = weights.argsort(1)
        output[indices < n] = 1
        output[~array_allowed.astype(bool)] = 0

        return output

    # ---- Handling door picking
    def set_picks(self, picks, add=False, allow_spoiled=False, n_per_row=None):

        # check for correct number of picks
        if n_per_row is not None:
            picks_per_row = picks.astype(int).sum(axis=1)
            wrong_n_picks = (picks_per_row != n_per_row)
            if np.any(wrong_n_picks):
                idx = np.argmax(wrong_n_picks)
                val = picks_per_row[idx]
                msg = ("Some trials have incorrect number of picks, e.g. "
                       f"on trial {idx}, there are {val} new picks "
                       f"but expected {n_per_row}.")
                self.bad_trials_raise(wrong_n_picks, msg, BadPick)

        # check for valid picks
        valid = self.validate_picks(picks)
        invalid_rows = np.any(~valid, axis=1)
        if not allow_spoiled and np.any(~valid):
            trial, door = self.get_index_success(~valid)
            msg = ("Revealed doors were picked, e.g. "
                   f"trial {trial} door {door}.")
            self.bad_trials_raise(invalid_rows, msg, BadPick)

        # mark spoiled games (only based on invalid picks)
        self.spoiled[invalid_rows] = 1

        # update sim.picked
        if add:
            picks = np.logical_or(picks, self.picked).astype(int)
        self.picked = picks

    def validate_picks(self, picks):
        return ~ np.logical_and(self.revealed, picks)

    # ---- Generic errors
    def bad_trials_raise(self, badrows, msg, errortype):
        idx = np.arange(len(badrows))[badrows]
        n = len(idx)
        raise errortype(f"{msg} Found for {n} trial(s):\n{idx}")

    # ---- Other helpers
    def get_index_success(self, boolarray, i=0):
        return np.asarray(np.where(boolarray)).T[i]

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


