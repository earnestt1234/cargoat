#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 16:10:27 2022

@author: earnestt1234
"""

from cargoat.actions.base import MontyHallAction
from cargoat.arrayops import get_index_success
from cargoat.errors import MontyHallError, bad_trials_raise

import numpy as np

def _verify_all_good_2D(sim, good_array, fail_message, action='raise'):

    invalid_rows = np.any(~good_array, axis=1)
    if np.all(good_array):
        return
    elif action == 'raise':
        trial, door = get_index_success(~good_array)
        msg = (f"{fail_message}, e.g. "
               f"trial {trial} door {door}.")
        bad_trials_raise(invalid_rows, msg, MontyHallError)
    elif action == 'spoil':
        sim.spoiled[invalid_rows] = 1
    elif action != 'nothing':
        raise ValueError('action must be one of "raise", "spoil", or "nothing".')

def _verify_all_good_1D(sim, good_array, fail_message, action='raise'):

    invalid = ~good_array
    if np.all(good_array):
        return
    elif action == 'raise':
        msg = (f"{fail_message}.")
        bad_trials_raise(invalid, msg, MontyHallError)
    elif action == 'spoil':
        sim.spoiled[invalid] = 1
    elif action != 'nothing':
        raise ValueError('action must be one of "raise", "spoil", or "nothing".')

class CheckSpoiled(MontyHallAction):
    def __init__(self, action='raise', revealed_picks=True,
                 revealed_cars=True, no_cars=True, multiple_picks=True):
        self.action = action
        self.revealed_picks = revealed_picks
        self.revealed_cars = revealed_cars
        self.no_cars = no_cars
        self.multiple_picks = multiple_picks

    def __call__(self, sim):

        if self.revealed_picks:
            good = ~np.logical_and(sim.picked, sim.revealed)
            _verify_all_good_2D(sim, good, fail_message='Found revealed & picked doors',
                                action=self.action)
        if self.revealed_cars:
            good = ~ np.logical_and(sim.cars, sim.revealed)
            _verify_all_good_2D(sim, good, fail_message='Found revealed cars',
                                action=self.action)
        if self.no_cars:
            good = sim.count_totals('cars') > 0
            _verify_all_good_1D(sim, good, fail_message='Found trials with no cars',
                                action=self.action)

        if self.multiple_picks:
            good = sim.count_totals('picked') <= 1
            _verify_all_good_1D(sim, good, fail_message='Found trials with multiple picked doors',
                                action=self.action)

class MarkSpoiled(MontyHallAction):
    def __call__(self, sim):
        sim.spoiled[True] = 1

class MarkUnspoiled(MontyHallAction):
    def __call__(self, sim):
        sim.spoiled[True] = 0
