#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 14:36:28 2022

@author: earnestt1234
"""

from cargoat.sim import combine_sims

class IfElse:
    def __init__(self, condition, a, b):
        self.condition = condition
        self.a = a
        self.b = b

    def __call__(self, sim):

        bools = self.condition(sim)
        sim_true = sim.select(x=bools)
        sim_false = sim.select(x=~bools)

        # print(bools)
        # print(sim_true.picked)
        # print(sim_false.picked)

        self.a(sim_true)
        self.b(sim_false)

        index = (~bools).astype(int)
        new = combine_sims([sim_true, sim_false], index=index)

        sim.picked = new.picked
        sim.revealed = new.revealed
        sim.cars = new.cars
        sim.spoiled = new.spoiled
