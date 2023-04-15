# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 18:33:21 2023

@author: earne
"""

import cargoat as cg
from cargoat import InitDoorsEmpty, InitDoorsFixed, InitDoorsRandom

class TestInitDoorsEmpty:

    init3 = InitDoorsEmpty(3)
    init0 = InitDoorsEmpty(0)
    initneg = InitDoorsEmpty(-2)
    initflt = InitDoorsEmpty(3.5)

    def make_sim(self):
        sim = cg.MontyHallSim(5)
        return sim

    def test_three_doors(self):
        sim = self.make_sim()
        self.init3(sim)
        assert sim.shape == (5, 3)

