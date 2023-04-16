# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 18:33:21 2023

@author: earne
"""

import numpy as np
import pytest

import cargoat as cg
from cargoat import InitDoorsEmpty, InitDoorsFixed, InitDoorsRandom

all_basic_inits = [InitDoorsEmpty(3),
                   InitDoorsFixed((1, 0, 0)),
                   InitDoorsRandom(cars=1, goats=2)]

class TestGeneral:

    def make_sim(self, n):
        sim = cg.MontyHallSim(n)
        return sim

    @pytest.mark.parametrize('init', all_basic_inits)
    def test_shape(self, init):
        sim = self.make_sim(5)
        init(sim)
        assert sim.shape == (5, 3)

    @pytest.mark.parametrize('init', all_basic_inits)
    def test_overwrite(self, init):
        sim = self.make_sim(5)
        sim.init_doors(20)
        init(sim)
        assert sim.shape == (5, 3)

    @pytest.mark.parametrize('init', all_basic_inits)
    def test_not_affect_picked_revealed(self, init):
        sim = self.make_sim(5)
        init(sim)
        assert np.all(sim.picked == 0) & np.all(sim.revealed == 0)

class TestInitDoorsEmpty:

    init3 = InitDoorsEmpty(3)
    init0 = InitDoorsEmpty(0)
    initneg = InitDoorsEmpty(-2)
    initflt = InitDoorsEmpty(3.5)

    def check_empty(self, sim):
        return (np.all(sim.picked == 0) &
                np.all(sim.cars == 0) &
                np.all(sim.revealed == 0))

    def make_sim(self):
        sim = cg.MontyHallSim(5)
        return sim

    def test_three_doors(self):
        sim = self.make_sim()
        self.init3(sim)
        assert sim.shape == (5, 3) and self.check_empty(sim)

    def test_zero_doors(self):
        sim = self.make_sim()
        self.init0(sim)
        assert sim.shape == (5, 0)

    def test_neg_doors(self):
        sim = self.make_sim()
        with pytest.raises(ValueError):
            self.initneg(sim)

class TestInitDoorsFixed:

    init_reg = InitDoorsFixed([1, 0, 0])

    def make_sim(self):
        sim = cg.MontyHallSim(5)
        return sim

    def test_car_placement(self):
        sim = self.make_sim()
        self.init_reg(sim)
        assert np.all(sim.cars[:, 0] == 1)

class TestInitDoorsRandom:

    def make_sim(self):
        sim = cg.MontyHallSim(5)
        return sim

    def test_regular_count(self):
        sim = self.make_sim()
        InitDoorsRandom(cars=1, goats=2)(sim)
        assert np.all(sim.cars.sum(axis=1) == 1)

    def test_all_cars_count(self):
        sim = self.make_sim()
        InitDoorsRandom(cars=3, goats=0)(sim)
        assert np.all(sim.cars.sum(axis=1) == 3)

    def test_all_goats_count(self):
        sim = self.make_sim()
        InitDoorsRandom(cars=0, goats=3)(sim)
        assert np.all(sim.cars.sum(axis=1) == 0)


