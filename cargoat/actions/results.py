#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes for finishing the game and reporting wins.
"""

import pprint

from cargoat.actions.base import MontyHallAction

class Finish(MontyHallAction):
    def __init__(self, spoiled_games='omit'):
        '''
        Print the number of wins and losses.

        Parameters
        ----------
        spoiled_games : str, optional
            Behavior for dealing with spoiled games. The default is 'omit'.
            - 'omit': discard spoiled games
            - 'include': include spoiled games in the results
            - 'only': only show the results for spoiled games

        Returns
        -------
        None.

        '''
        self.spoiled_games = spoiled_games

    def __call__(self, sim):
        pprint.pprint(sim.get_results(spoiled_games=self.spoiled_games), sort_dicts=False)
        return sim
