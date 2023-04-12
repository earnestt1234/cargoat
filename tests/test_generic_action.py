#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 21:42:30 2023

@author: earnestt1234
"""

import numpy as np
import pytest

import cargoat as cg

main_arrays = ['cars', 'revealed', 'picked']

class TestPickOneDoor:

    def generate_sim(self, target):
        sim = cg.MontyHallSim(n=1000)
        sim.init_doors(3)

        action = cg.actions.generic.GenericAction(target=target,
                                                  doors=1,
                                                  behavior='overwrite')
        action(sim)
        return sim

    @pytest.mark.parametrize("target", main_arrays)
    def test_one_selected(self, target):
        sim = self.generate_sim(target)
        arr = getattr(sim, target)
        trial_counts = arr.sum(axis=1)
        assert np.all(trial_counts == 1)



