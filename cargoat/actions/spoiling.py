#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes for dealing with manual marking of spoiled games.
"""

from cargoat.actions.base import MontyHallAction
from cargoat.arrayops import get_index_success
from cargoat.errors import MontyHallError, bad_trials_raise

import numpy as np

def _verify_all_good_2D(sim, good_array, fail_message, behavior='raise'):
    '''Check a boolean 2D array is all True, report error if not.'''
    invalid_rows = np.any(~good_array, axis=1)
    if np.all(good_array):
        return
    elif behavior == 'raise':
        trial, door = get_index_success(~good_array)
        msg = (f"{fail_message}, e.g. "
               f"trial {trial} door {door}.")
        bad_trials_raise(invalid_rows, msg, MontyHallError)
    elif behavior == 'spoil':
        sim.spoiled[invalid_rows] = 1
    elif behavior != 'nothing':
        raise ValueError('action must be one of "raise", "spoil", or "nothing".')

def _verify_all_good_1D(sim, good_array, fail_message, behavior='raise'):
    '''Check a boolean 1D array is all True, report error if not.'''
    invalid = ~good_array
    if np.all(good_array):
        return
    elif behavior == 'raise':
        msg = (f"{fail_message}.")
        bad_trials_raise(invalid, msg, MontyHallError)
    elif behavior == 'spoil':
        sim.spoiled[invalid] = 1
    elif behavior != 'nothing':
        raise ValueError('action must be one of "raise", "spoil", or "nothing".')

class CheckSpoiled(MontyHallAction):
    def __init__(self, behavior='raise', revealed_picks=True,
                 revealed_cars=True, no_cars=False, multiple_picks=False):
        '''
        Manually check if any of the games are spoiled.

        By default, this only checks if there are revealed cars or picked
        doors that are revealed.  If all actions are applied with
        `allow_spoiled=False`, then no games should be spoiled.  If some
        steps are applied with `allow_spoiled=True`, this can manually
        check and alert to that.

        This can also check for other game states with may be considered
        spoiled (no cars present, or multiple doors picked.)

        Parameters
        ----------
        action : str, optional
            Protocol when spoiled games are detected. The default is 'raise',
            which raises an Error.  Other options are 'spoil' (mark the
            problem trials as spoiled, but don't stop the simulation) or
            'nothing' (do nothing).
        revealed_picks : bool, optional
            Detect trials with revealed picked doors. The default is True.
        revealed_cars : bool, optional
            Detect trials with revealed cars. The default is True.
        no_cars : bool, optional
            Detect trials with no cars. The default is False.
        multiple_picks : bool, optional
            Detect trials with multiple picked doors. The default is False.

        Returns
        -------
        None.

        '''
        self.behavior = behavior
        self.revealed_picks = revealed_picks
        self.revealed_cars = revealed_cars
        self.no_cars = no_cars
        self.multiple_picks = multiple_picks

    def __call__(self, sim):

        if self.revealed_picks:
            good = ~np.logical_and(sim.picked, sim.revealed)
            _verify_all_good_2D(sim, good, fail_message='Found revealed & picked doors',
                                behavior=self.behavior)
        if self.revealed_cars:
            good = ~ np.logical_and(sim.cars, sim.revealed)
            _verify_all_good_2D(sim, good, fail_message='Found revealed cars',
                                behavior=self.behavior)
        if self.no_cars:
            good = sim.count_totals('cars') > 0
            _verify_all_good_1D(sim, good, fail_message='Found trials with no cars',
                                behavior=self.behavior)

        if self.multiple_picks:
            good = sim.count_totals('picked') <= 1
            _verify_all_good_1D(sim, good, fail_message='Found trials with multiple picked doors',
                                behavior=self.behavior)

        return sim

class MarkSpoiled(MontyHallAction):
    '''Manually mark all trials as spoiled.  Can be combined with
    `cargoat.actions.logical.IfElse` for conditional marking.'''
    def __call__(self, sim):
        sim.spoiled[True] = 1
        return sim

class MarkUnspoiled(MontyHallAction):
    '''Manually mark all trials as unspoiled.  Can be combined with
    `cargoat.actions.logical.IfElse` for conditional marking.'''
    def __call__(self, sim):
        sim.spoiled[True] = 0
        return sim
