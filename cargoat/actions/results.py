#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 12:26:23 2022

@author: earnestt1234
"""

import pprint

from cargoat.actions.base import MontyHallAction

class Finish(MontyHallAction):
    def __init__(self, spoiled_games = 'omit'):
        self.spoiled_games = spoiled_games

    def __call__(self, sim):
        pprint.pprint(sim.get_results(spoiled_games=self.spoiled_games), sort_dicts=False)
