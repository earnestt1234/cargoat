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

class TestIfElse:

    def make_sim(self):
        sim = cg.MontyHallSim(1000)
        sim.init_doors(3)
        return sim

    def test_callable(self):
        sim = self.make_sim()
        sim.cars[:500, :] = 1

        condition = lambda x: x.cars.sum(axis=1) > 0

        a = cg.Pick()
        b = cg.Pass()

        action = cg.IfElse(condition, a, b, condition_call=True)
        action(sim)

        assert np.all(sim.count_totals('picked') == np.repeat([1, 0], [500, 500]))

    def test_not_callable(self):
        sim = self.make_sim()
        sim.cars[:500, :] = 1

        condition = np.repeat([True, False], [500, 500])

        a = cg.Pick()
        b = cg.Pass()

        action = cg.IfElse(condition, a, b, condition_call=False)
        action(sim)

        assert np.all(sim.count_totals('picked') == np.repeat([1, 0], [500, 500]))

class TryExcept:

    def make_sim(self):
        sim = cg.MontyHallSim(1000)
        sim.init_doors(3)
        return sim

    def test_fail(self):

        a = lambda x : 1/0
        b = cg.Pick()

        sim = self.make_sim()
        action = cg.TryExcept(a, b)
        action(sim)

        assert np.all(sim.count_totals('picked') == 1)

    def test_no_fail(self):

        a = cg.Reveal()
        b = cg.Pick()

        sim = self.make_sim()
        action = cg.TryExcept(a, b)
        action(sim)

        assert np.all(sim.count_totals('picked') == 0) and np.all(sim.count_totals('revealed') == 1)
