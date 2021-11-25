#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for the cargoat `MontyHallSimulation` class, which is used for
running a given Monty Hall experiment many times.
"""

import numpy as np

from .errors import BadPick

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
        if exclude_current:
            return (~np.logical_or(self.picked, self.revealed)).astype(int)
        else:
            return 1 - self.revealed

    def revealable_doors(self):
        rd = ~np.logical_or.reduce([self.cars, self.picked, self.revealed])
        return rd.astype(int)

    # ---- Handling door picking
    def set_picks(self, picks, add=False, allow_spoiled=True):
        valid = self.validate_picks(picks)
        badrows = np.any(~valid, axis=1)
        if not allow_spoiled and np.any(~valid):
            trial, door = self.get_index_success(~valid)
            msg = ("Revealed doors were picked, e.g. "
                   f"trial {trial} door {door}.")
            self.bad_trials_raise(badrows, msg, BadPick)

        self.spoiled[badrows] = 1
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


