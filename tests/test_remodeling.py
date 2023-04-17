#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 18:33:48 2023

@author: earnestt1234
"""

import numpy as np
import pytest

import cargoat as cg

class TestAddDoors:

    def make_sim(self):
        sim = cg.MontyHallSim(5)
        sim.init_doors(3)
        sim.cars[:] = 1
        return sim

    def test_add_with_int(self):
        sim = self.make_sim()
        cg.AddDoors(0)(sim)
        assert sim.shape == (5, 4) and sim.cars[:, 0].sum() == 0

    def test_add_with_list(self):
        sim = self.make_sim()
        cg.AddDoors([0])(sim)
        assert sim.shape == (5, 4) and sim.cars[:, 0].sum() == 0

    def test_add_multiple(self):
        sim = self.make_sim()
        cg.AddDoors([0, 3])(sim)
        assert (sim.shape == (5, 5) and
                sim.cars[:, 0].sum() == 0 and
                sim.cars[:, 4].sum() == 0)

    def test_out_of_bounds(self):
        sim = self.make_sim()
        with pytest.raises(IndexError):
            cg.AddDoors([0, 10])(sim)

class TestRemoveDoors:

    def make_sim(self):
        sim = cg.MontyHallSim(5)
        sim.init_doors(3)
        sim.cars[:] = 1
        return sim

    def test_remove_with_int(self):
        sim = self.make_sim()
        cg.RemoveDoors(0)(sim)
        assert sim.shape == (5, 2)

    def test_remove_with_list(self):
        sim = self.make_sim()
        cg.RemoveDoors([0])(sim)
        assert sim.shape == (5, 2)

    def test_remove_mutliple(self):
        sim = self.make_sim()
        cg.RemoveDoors([0, 1])(sim)
        assert sim.shape == (5, 1)

    def test_out_of_bounds(self):
        sim = self.make_sim()
        with pytest.raises(IndexError):
            cg.RemoveDoors([0, 10])(sim)

class TestRearrangeDoors:

    def make_sim(self):
        sim = cg.MontyHallSim(5)
        sim.init_doors(3)
        sim.cars[:, 1] = 1
        sim.cars[:, 2] = 2
        return sim

    def test_rearrange(self):
        sim = self.make_sim()
        cg.RearrangeDoors([2, 1, 0])(sim)
        assert np.all(sim.cars.mean(axis=0) == [2, 1, 0])
