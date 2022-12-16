#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 14:36:28 2022

@author: earnestt1234
"""

from cargoat.actions.convenience import Pass
from cargoat.actions.base import MontyHallAction
from cargoat.sim import combine_sims

import numpy as np

class ChanceTo(MontyHallAction):
    def __init__(self, p, action):
        self.p = p
        self.action = action

    def __call__(self, sim):
        draws = np.random.rand(len(sim.idx))
        action = IfElse(draws < self.p, self.action, Pass(), call=False)
        action(sim)

class IfElse(MontyHallAction):
    def __init__(self, condition, a, b, call=True):
        self.condition = condition
        self.a = a
        self.b = b
        self.call = call

    def __call__(self, sim):

        bools = self.condition(sim) if self.call else self.condition
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

class TryExcept(MontyHallAction):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self, sim):
        temp = sim.copy()
        try:
            self.a(sim)
        except:
            self.b(temp)
            sim.picked=temp.picked
            sim.cars=temp.cars
            sim.revealed=temp.revealed
            sim.spoiled=temp.spoiled
