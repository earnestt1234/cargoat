#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for the cargoat `MontyHallSimulation` class, which is used for
running a given Monty Hall experiment many times.
"""

import numpy as np

class MontyHallSim:
    def __init__(self, n):
        self.n = n

        self.cars = np.empty(0)
        self.picked = np.empty(0)
        self.revealed = np.empty(0)

    @property
    def idx(self):
        return np.arange(self.n)

    @property
    def shape(self):
        return self.cars.shape

    def pickable_doors(self, exclude_current=True):
        if exclude_current:
            return 1 - (self.picked + self.revealed)
        else:
            return 1 - self.revealed

    def revealable_doors(self):
        rd = ~np.logical_or.reduce([self.cars, self.picked, self.revealed])
        return rd.astype(int)

    def validate_picks(self, picks):
        return ~ np.logical_and(self.revealed, picks)

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