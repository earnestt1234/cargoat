#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 22:09:37 2023

@author: earnestt1234
"""

import numpy as np
import pytest

import cargoat as cg

class TestCheckSpoiled:

    def make_sim(self):
        sim = cg.MontyHallSim(3)
        sim.init_doors(3)
        return sim

    @pytest.mark.parametrize('behavior', ['spoil', 'raise'])
    def test_revealed_picks(self, behavior):
        sim = self.make_sim()
        sim.picked[0, 0] = 1
        sim.revealed[0, 0] = 1
        action = cg.CheckSpoiled(revealed_picks=True, behavior=behavior)
        if behavior == 'raise':
            with pytest.raises(cg.errors.MontyHallError):
                action(sim)
        elif behavior == 'spoil':
            action(sim)
            assert np.all(sim.spoiled == [1, 0, 0])

    @pytest.mark.parametrize('behavior', ['spoil', 'raise'])
    def test_revealed_cars(self, behavior):
        sim = self.make_sim()
        sim.revealed[0, 0] = 1
        sim.cars[0, 0] = 1
        action = cg.CheckSpoiled(revealed_picks=True, behavior=behavior)
        if behavior == 'raise':
            with pytest.raises(cg.errors.MontyHallError):
                action(sim)
        elif behavior == 'spoil':
            action(sim)
            assert np.all(sim.spoiled == [1, 0, 0])

    @pytest.mark.parametrize('behavior', ['spoil', 'raise'])
    def test_no_cars(self, behavior):
        sim = self.make_sim()
        action = cg.CheckSpoiled(no_cars=True, behavior=behavior)
        if behavior == 'raise':
            with pytest.raises(cg.errors.MontyHallError):
                action(sim)
        elif behavior == 'spoil':
            action(sim)
            assert np.all(sim.spoiled == [1, 1, 1])

    @pytest.mark.parametrize('behavior', ['spoil', 'raise'])
    def test_multiple_picks(self, behavior):
        sim = self.make_sim()
        sim.picked[:] = 1
        action = cg.CheckSpoiled(multiple_picks=True, behavior=behavior)
        if behavior == 'raise':
            with pytest.raises(cg.errors.MontyHallError):
                action(sim)
        elif behavior == 'spoil':
            action(sim)
            assert np.all(sim.spoiled == [1, 1, 1])
