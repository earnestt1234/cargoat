#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 23:00:59 2022

@author: earnestt1234
"""

import numpy as np
import pytest

import cargoat as cg

class Test_Sim_Initialization_N:

    # ---- Errors
    def test_string_n_non_numeric(self):
        with pytest.raises(ValueError):
            cg.MontyHallSim('a')

    def test_string_n_float(self):
        with pytest.raises(ValueError):
            cg.MontyHallSim('1.2')

    # ---- No errors
    def test_string_n_integer(self):
        sim = cg.MontyHallSim('10')
        assert isinstance(sim, cg.MontyHallSim) and sim.n == 10

    def test_n_integer(self):
        sim = cg.MontyHallSim(10)
        assert isinstance(sim, cg.MontyHallSim) and sim.n == 10

    def test_n_float(self):
        sim = cg.MontyHallSim(10.9)
        assert isinstance(sim, cg.MontyHallSim) and sim.n == 10

    def test_n_negative_int(self):
        sim = cg.MontyHallSim(-10)
        assert isinstance(sim, cg.MontyHallSim) and sim.n == -10

class Test_Sim_Empty:

    def test_init_empty(self):
        sim = cg.MontyHallSim(10)
        assert sim.empty

    @pytest.mark.parametrize("s", ["cars", "revealed", "picked", 'spoiled'])
    def test_populate_array_not_empty(self, s):
        sim = cg.MontyHallSim(10)
        setattr(sim, s, np.array([[1]]))
        assert not sim.empty

