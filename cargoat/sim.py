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

def combine_sims(sims, index=None, copy=True):

    n = len(sims)
    rows = [x.shape[0] for x in sims]
    cols = [x.shape[1] for x in sims]
    copyfun = (lambda x: x.copy()) if copy else (lambda x: x)

    if len(set(cols)) != 1:
        raise ValueError('All sims must have the same number of doors (columns).')

    if index is None:
        index = np.repeat(np.arange(n, dtype=int), rows)

    shape = (len(index), cols[0])

    cars = np.zeros(shape, dtype=int)
    picked = np.zeros(shape, dtype=int)
    revealed = np.zeros(shape, dtype=int)
    spoiled = np.zeros(shape[0], dtype=int)

    for i in np.unique(index):
        sim = sims[i]
        cars[index == i, :] = copyfun(sim.cars)
        picked[index == i, :] = copyfun(sim.picked)
        revealed[index == i, :] = copyfun(sim.revealed)
        spoiled[index == i] = sim.spoiled

    return MontyHallSim.from_arrays(picked=picked,
                                    revealed=revealed,
                                    cars=cars,
                                    spoiled=spoiled,
                                    copy=False)

class MontyHallSim:
    '''Class for remembering the status of the game simualtion.'''

    def __init__(self, n):
        '''
        The MontyHallSim object tracks the game status for repeated Monty Hall
        games.

        Games are mainly recorded with numpy arrays.  There are three primary
        arrays, stored as attributes:
            - `self.picked`: Indicates doors selected by the player
            - `self.revealed`: Indicates doors that have been opened
            - `self.cars`: Indicates doors which have a car behind them.

        These are all binary, 2D, integer arrays.  The shape of the arrays
        during/after a typical simulation will be (trials, doors) - one row
        constitutes one game.  The initialization argument `n` determines
        the number of trials.  The number of doors is determined by the particular
        game being played.

        There is also a `spoiled` attribute, which is a numpy array of
        shape (trials,).  This simply records whether a trial has broken
        the rules of the traditional Monty Hall game.

        MontyHallSims are updated by applying rules/steps, i.e. from the
        `cargoat.steps` subpackage.

        Typically, a user *should not* have to manually define a MontyHallSim
        object, as `cargoat.core.play` will do this provided a list of steps.
        *Initialization of a MontyHallSim results in an empty simulation* -
        i.e. all the array attributes will be empty.  The steps in
        `cargoat.steps.initialization` are intended for populating the
        simulation.


        Parameters
        ----------
        n : int
            Number of trials to simulate.

        Returns
        -------
        None.

        '''
        self.n = n

        self.cars = np.empty(0)
        self.picked = np.empty(0)
        self.revealed = np.empty(0)
        self.spoiled = np.empty(0)

    # ---- Class methods

    @classmethod
    def from_arrays(cls, picked=None, revealed=None, cars=None,
                    spoiled=None, default=0, copy=True):
        '''
        Construct a MontyHallSim from existing numpy arrays.

        Parameters
        ----------
        picked : 2D numpy array, optional
            Integer array indicating picked doors. The default is None.
        revealed : 2D numpy array, optional
            Integer array indicating revealed doors. The default is None.
        cars : 2D numpy array, optional
            Integer array indicating doors containing cars. The default is None.
        spoiled : 1D numpy array, optional
            Integer array indicating spoiled trials. The default is None.
        default : int, optional
            When only some of `picked`/`revealed`/`cars` are provided, use
            this value to fill the missing arrays. The default is 0.
        copy : bool, optional
            Call an explicit copy on the arrays before binding to the new
            simulation being created. Intended to prevent multiple simulations
            pointing to the same arrays.  The default is True.

        Raises
        ------
        ValueError
            - Didn't provide at least one of `cars`, `picked`, or `revealed`
            - Different array shapes for provided arrays.

        Returns
        -------
        out : MontyHallSim
            New simulation object.

        '''

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
        '''Return a numpy arange of length `self.n`'''
        return np.arange(self.n)

    @property
    def shape(self):
        '''Return the dimensions of the simulation (trials, doors).  Throws an error if
        different array shapes are found.'''
        shape_set = set([self.cars.shape, self.picked.shape, self.revealed.shape])
        if len(shape_set) != 1:
            raise RuntimeError('Found different shapes for simulation arrays!')

        return self.picked.shape

    # ---- Indexing
    def select(self, x=None, y=None, copy=True):
        '''
        Index the simulation to create a new one.

        Parameters
        ----------
        x : int, float, list-like, optional
            Indexer for trials (rows) of simulation. The default is None,
            in which case all trials are selected.
        y : int, float, list-like, optional
            Indexer for doors (columns) of simulation. The default is None,
            in which case all doors are selected.
        copy : bool, optional
            Create an explicit copy of the arrays before binding to the
            newly created simulation. The default is True.

        Returns
        -------
        MontyHallSimulation
            New simulation object.

        '''
        x = slice(None) if x is None else x
        y = slice(None) if y is None else y
        copyfun = (lambda x: x.copy()) if copy else (lambda x: x)

        cars = copyfun(self.cars[x, y])
        picked = copyfun(self.picked[x, y])
        revealed = copyfun(self.revealed[x, y])
        spoiled = copyfun(self.spoiled[x])

        return self.from_arrays(picked=picked,
                                revealed=revealed,
                                cars=cars,
                                spoiled=spoiled,
                                copy=False)


    # ---- Status of the sim
    def pickable_doors(self, exclude_current=True):
        '''Array of the simulation shape indicating which doors are
        not revealed (with or without the current picked doors).'''
        return ~self.query_doors_or(picked=exclude_current, revealed=True)

    def query_doors_or(self, cars=False, picked=False, revealed=False,
                       not_cars=False, not_picked=False, not_revealed=False):
        '''
        Return a boolean array indicating which doors of the simulation
        meet one or more conditions.

        Parameters
        ----------
        cars : bool, optional
            Signal doors containing cars. The default is False.
        picked : bool, optional
            Signal doors that are picked. The default is False.
        revealed : bool, optional
            Signal doors that are revealed. The default is False.
        not_cars : bool, optional
            Signal doors that do not contain cars. The default is False.
        not_picked : bool, optional
            Signal doors that are not picked. The default is False.
        not_revealed : bool, optional
            Signal doors that are closed. The default is False.

        Returns
        -------
        out : numpy array

        '''
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
        '''Array of the simulation shape indicating which doors are
        not revealed, don't contain cars, and aren't currently picked.'''
        return ~self.query_doors_or(cars=True, picked=True, revealed=True)

    def count_totals(self, target):
        '''Return a count of the number of positives for each trial in the
        simulation.  Target is `cars`, `picked`, or `revealed`. '''
        arr = getattr(self, target)
        return arr.sum(axis=1)

    # ---- Generic setter functions

    def _get_spoiling_func(self, target):
        '''Helper to return the function used to detect spoiled games when
        applying certain steps.'''
        if target == 'picked':
            return self._check_spoiling_picks

        elif target == 'revealed':
            return self._check_spoiling_reveals

        elif target == 'cars':
            return self._check_spoiling_cars

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
            valid = np.full(self.shape, True)

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

    # ---- Car placing
    def _check_spoiling_cars(self, cars, behavior, allow_spoiled=True):
        # car placement/removal is not really mentioned in the
        # typical game variations
        # for now, treating changing the car array as unable to spoil
        valid = np.full(self.shape, True)
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

    def copy(self):
        return self.from_arrays(picked=self.picked,
                                revealed=self.revealed,
                                cars=self.cars,
                                spoiled=self.spoiled,
                                copy=True)

    # ---- Results
    def get_results(self, spoiled_games='omit'):

        spoiled = self.spoiled == 1
        if spoiled_games == 'include':
            sim = self
        elif spoiled_games == 'omit':
            sim = self.select(~spoiled)
        elif spoiled_games == 'only':
            sim = self.select(spoiled)
        else:
            raise ValueError('`spoiled_games` must be "include", "omit", or "only".')

        wins = np.sum(np.any(sim.picked * sim.cars, axis=1))
        losses = sim.n - wins
        percent_wins = (wins / sim.n) * 100
        percent_losses = (losses / sim.n) * 100
        results = {
            'trials': sim.n,
            'wins': wins,
            'losses': losses,
            'percent_wins': percent_wins,
            'percent_losses': percent_losses
            }

        return results


