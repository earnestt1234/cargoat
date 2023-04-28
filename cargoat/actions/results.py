#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes for finishing the game and reporting wins.
"""

import pprint

from cargoat.actions.base import MontyHallAction

class ShowResults(MontyHallAction):
    def __init__(self, condition=None, condition_call=True):
        '''
        Print the number of wins and losses.

        Parameters
        ----------
        condition :  callable or list-like
            Use this argument to show result for only certain trials.
            By default, this is expected to be a callable.  The callable is
            passed the current simulation, and is expected to return a boolean
            1D array which dictates the rows/trials to include.

            A pre-computed condition can be applied by passing
            `condition_call=False` - in this case, `condition` will not be called,
            it will simply be used to index the simulation.
        call : bool, optional
            Treat `condition` as a callable. The default is True.

        Returns
        -------
        None.

        '''
        self.condition = condition
        self.condition_call = condition_call

    def __call__(self, sim):
        condition_call = False if self.condition is None else self.condition_call
        bools = self.condition(sim) if condition_call else self.conditon
        res = sim.get_results(condition=bools)
        pprint.pprint(res, sort_dicts=False)
        return sim
