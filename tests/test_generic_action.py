#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 21:42:30 2023

@author: earnestt1234
"""

from itertools import chain, combinations

import numpy as np
import pandas as pd
import pytest

import cargoat as cg
from cargoat.actions.generic import GenericAction as GA

main_arrays = ['cars', 'revealed', 'picked']

# https://docs.python.org/3/library/itertools.html#itertools-recipes
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

RESULTS = []

class TestPickCounts:

    # ---- helpers
    def check_count(self, sim, target, expected):
        arr = getattr(sim, target)
        row_counts = arr.astype(bool).sum(axis=1)
        return np.all(row_counts == expected)

    def generate_sim(self, target):
        sim = cg.MontyHallSim(n=1000)
        sim.init_doors(3)
        return sim

    def log_results(self, name, sim, target, expected):
        arr = getattr(sim, target)
        a, b, c = arr.sum(axis=0)
        results = {'trial':name,
                   'exp1': int(expected[0] * sim.n),
                   'obs1':a,
                   'exp2': int(expected[1] * sim.n),
                   'obs2':b,
                   'exp3': int(expected[2] * sim.n),
                   'obs3':c}
        RESULTS.append(results)

    # ---- tests
    @pytest.mark.parametrize("target", main_arrays)
    def test_one_door(self, target):
        sim = self.generate_sim(target)
        action = GA(target, doors=1, weighted=False, behavior='overwrite')
        action(sim)
        self.log_results(f'one_door_{target}', sim, target, [1/3, 1/3, 1/3])
        assert self.check_count(sim, target, 1)

    @pytest.mark.parametrize("target", main_arrays)
    def test_two_doors(self, target):
        sim = self.generate_sim(target)
        action = GA(target, doors=2, weighted=False, behavior='overwrite')
        action(sim)
        self.log_results(f'two_door_{target}', sim, target, [2/3, 2/3, 2/3])
        assert self.check_count(sim, target, 2)

    @pytest.mark.parametrize("target", main_arrays)
    def test_three_doors(self, target):
        sim = self.generate_sim(target)
        action = GA(target, doors=3, weighted=False, behavior='overwrite')
        action(sim)
        self.log_results(f'three_door_{target}', sim, target, [1, 1, 1])
        assert self.check_count(sim, target, 3)

    @pytest.mark.parametrize("target", main_arrays)
    def test_four_doors(self, target):
        sim = self.generate_sim(target)
        action = GA(target, doors=4, weighted=False, behavior='overwrite')
        with pytest.raises(Exception):
            action(sim)

    @pytest.mark.parametrize("doors", powerset([0, 1, 2]))
    @pytest.mark.parametrize("target", main_arrays)
    def test_door_list(self, target, doors):
        sim = self.generate_sim(target)
        action = GA(target, doors=doors, weighted=False, behavior='overwrite')
        action(sim)
        expected = [1 if i in doors else 0 for i in range(3)]
        self.log_results(f'list_door_{target}', sim, target, expected)
        assert self.check_count(sim, target, len(doors))

    @pytest.mark.parametrize("target", main_arrays)
    def test_weights_even(self, target):
        sim = self.generate_sim(target)
        action = GA(target, doors=[1, 1, 1], weighted=True, behavior='overwrite')
        action(sim)
        self.log_results(f'weight_door_even_{target}', sim, target, [1/3, 1/3, 1/3])
        assert self.check_count(sim, target, 1)

    @pytest.mark.parametrize("target", main_arrays)
    def test_weights_100(self, target):
        sim = self.generate_sim(target)
        action = GA(target, doors=[1, 0, 0], weighted=True, behavior='overwrite')
        action(sim)
        self.log_results(f'weight_door_100_{target}', sim, target, [1, 0, 0])
        assert self.check_count(sim, target, 1)

    @pytest.mark.parametrize("target", main_arrays)
    def test_weights_skew(self, target):
        sim = self.generate_sim(target)
        action = GA(target, doors=[.8, .1, .1], weighted=True, behavior='overwrite')
        action(sim)
        self.log_results(f'weight_door_skew_{target}', sim, target, [.8, .1, .1])
        assert self.check_count(sim, target, 1)

    def test_print_results(self, capsys):
        df = pd.DataFrame(RESULTS)
        with capsys.disabled():
            print()
            print("OBSERVED VS EXPECTED DOOR COUNTS")
            print('--------------------------------')
            print(df)
            print()
        assert True

