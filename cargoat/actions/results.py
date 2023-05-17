#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes for finishing the game and reporting wins.
"""

import pprint

from cargoat.actions.base import MontyHallAction

import numpy as np

class ShowResults(MontyHallAction):
    def __init__(self, spoiled_games=None, condition=None, condition_call=True):
        '''
        Print the number of wins and losses.

        Parameters
        ----------
        spoiled_games: str
            Convenience option for dealing with spoiled games.  Options are:

                - 'ignore': get results for all trial
                - 'omit': don't include spoiled games
                - 'only': only include results for spoiled games
                - None: use a user-specified condition if provided

            When specified, the `condition` and `condition_call` arguments
            are ignored.

        condition :  callable or list-like
            Use this argument to show result for only certain trials.
            By default, this is expected to be a callable.  The callable is
            passed the current simulation, and is expected to return a boolean
            1D array which dictates the rows/trials to include.

            A pre-computed condition can be applied by passing
            `condition_call=False` - in this case, `condition` will not be called,
            it will simply be used to index the simulation.
        condition_call : bool, optional
            Treat `condition` as a callable. The default is True.

        Returns
        -------
        None.

        '''
        self.spoiled_games = spoiled_games
        self.condition = condition
        self.condition_call = condition_call

    def _get_spoiled_games_condition(self, sim):
        if self.spoiled_games == 'ignore':
            bools = np.ones(sim.n, dtype=bool)
        elif self.spoiled_games == 'omit':
            bools = ~sim.spoiled
        elif self.spoiled_games == 'only':
            bools = sim.spoiled
        else:
            raise ValueError('`spoiled_games` must be "ignore", "omit", or "only".')
        return bools

    def __call__(self, sim):
        if self.spoiled_games is not None:
            bools = self._get_spoiled_games_condition(sim)
        else:
            condition_call = False if self.condition is None else self.condition_call
            bools = self.condition(sim) if condition_call else self.condition
        res = sim.get_results(condition=bools)
        pprint.pprint(res, sort_dicts=False)
        return sim
