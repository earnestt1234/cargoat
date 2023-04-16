#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 19:32:00 2023

@author: earnestt1234
"""

import cargoat as cg

import numpy as np

class TestChanceTo:

    def make_sim(self):
        sim = cg.MontyHallSim(1000)
        sim.init_doors(3)
        return sim

    def test_always(self):
        action = cg.ChanceTo(1, cg.Pick())
        sim = self.make_sim()
        action(sim)
        assert np.all(sim.picked.astype(bool).sum(axis=1) == 1)

    def test_never(self):
        action = cg.ChanceTo(0, cg.Pick())
        sim = self.make_sim()
        action(sim)
        assert np.all(sim.picked.astype(bool).sum(axis=1) == 0)

    def test_sometimes(self):
        # note: extremely small chance this fails !
        action = cg.ChanceTo(0.5, cg.Pick())
        sim = self.make_sim()
        action(sim)
        assert np.all(0 < sim.picked.astype(bool).sum(axis=1).sum() < 1000)
