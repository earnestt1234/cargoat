#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 23:00:59 2022

@author: earnestt1234
"""

import numpy as np
import pytest

import cargoat as cg

main_arrays = ['cars', 'revealed', 'picked']
all_arrays = main_arrays + ['spoiled']

class TestSimInitializationN:

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

class TestSimEmpty:

    def test_init_empty(self):
        sim = cg.MontyHallSim(10)
        assert sim.empty

    @pytest.mark.parametrize("s", main_arrays)
    def test_populate_array_not_empty(self, s):
        sim = cg.MontyHallSim(10)
        setattr(sim, s, np.array([[1]]))
        assert not sim.empty

    @pytest.mark.parametrize("a", main_arrays)
    def test_make_empty(self, a):
        sim = cg.MontyHallSim(10)
        sim.init_doors(3)
        shape_prior = sim.shape
        sim.make_empty()
        assert (shape_prior == (10, 3)) and sim.empty

class TestSimFromArrays:

    def test_no_main_arrays(self):
        with pytest.raises(ValueError):
            cg.MontyHallSim.from_arrays(cars=None, picked=None, revealed=None)

    @pytest.mark.parametrize("a", main_arrays)
    def test_sim_one_array(self, a):
        init_args = {a: np.ones((3, 3), dtype=int)}
        sim = cg.MontyHallSim.from_arrays(**init_args)
        assert all(getattr(sim, x).shape == (3, 3) for x in main_arrays)

    def test_sim_all_arrays(self):
        a = np.ones((10, 5), dtype=int)
        sim = cg.MontyHallSim.from_arrays(picked = a, revealed = a, cars = a,
                                          spoiled = a[:, 0])
        assert all(getattr(sim, x).shape == (10, 5) for x in main_arrays)

    def test_sim_mixed_shape(self):
        a = np.ones((4, 3), dtype=int)
        b = np.ones((4, 4), dtype=int)
        with pytest.raises(ValueError):
            cg.MontyHallSim.from_arrays(picked=a, cars=b)

    @pytest.mark.parametrize("default", [0, 1])
    def test_default(self, default):
        sim = cg.MontyHallSim.from_arrays(picked = np.ones((3, 3), dtype=int), default=default)
        assert (sim.cars == default).all() and (sim.revealed == default).all()

    def test_non_binary_arrays(self):
        with pytest.warns(RuntimeWarning):
            cg.MontyHallSim.from_arrays(picked = np.random.rand(3, 3))

    def test_copy(self):
        a = np.ones((10, 5), dtype=int)
        sim = cg.MontyHallSim.from_arrays(picked = a, copy=True)
        a[0, 0] = 42
        assert sim.picked[0, 0] == 1

    def test_no_copy(self):
        a = np.ones((10, 5), dtype=int)
        sim = cg.MontyHallSim.from_arrays(picked = a, copy=False)
        a[0, 0] = 42
        assert sim.picked[0, 0] == 42

    def test_pass_spoiled(self):
        a = np.ones((10, 5), dtype=int)
        spoiled = np.zeros(10, dtype=int)
        sim = cg.MontyHallSim.from_arrays(picked = a, spoiled=spoiled)
        assert (sim.spoiled == np.zeros(10, dtype=int)).all()

    def test_pass_spoiled_bad_size(self):
        a = np.ones((10, 5), dtype=int)
        spoiled = np.zeros(9, dtype=int)
        with pytest.raises(ValueError):
            cg.MontyHallSim.from_arrays(picked = a, spoiled=spoiled)

    def test_pass_spoiled_only(self):
        spoiled = np.zeros(9, dtype=int)
        with pytest.raises(ValueError):
            cg.MontyHallSim.from_arrays(spoiled=spoiled)

class TestIdxShape:

    @pytest.mark.parametrize("n", [1, 10, 100000])
    def test_idx(self, n):
        sim = cg.MontyHallSim(n)
        sim.init_doors(4)
        assert (sim.idx == np.arange(n)).all()

    @pytest.mark.parametrize("n", [1, 10, 100000])
    def test_shape_good(self, n):
        sim = cg.MontyHallSim(n)
        sim.init_doors(4)
        assert (sim.shape == (n, 4))

    def test_shape_bad(self):
        sim = cg.MontyHallSim(100)
        sim.init_doors(4)
        sim.picked = np.ones((6, 7))
        with pytest.raises(RuntimeError):
            sim.shape

class TestSelect:

    @pytest.mark.filterwarnings('ignore:Non-binary')
    def test_select_single_door(self):
        sim = cg.MontyHallSim(3)
        sim.init_doors(3)
        sim.picked = np.arange(9).reshape((3, 3))
        new = sim.select(x=None, y=0, copy=True)
        assert (new.picked.sum() == 0 + 3 + 6)

    @pytest.mark.filterwarnings('ignore:Non-binary')
    def test_select_multiple_doors(self):
        sim = cg.MontyHallSim(3)
        sim.init_doors(3)
        sim.picked = np.arange(9).reshape((3, 3))
        new = sim.select(x=None, y=[0, 1], copy=True)
        assert (new.picked.sum() == 0 + 3 + 6 + 1 + 4 + 7)

    @pytest.mark.filterwarnings('ignore:Non-binary')
    def test_select_single_trial(self):
        sim = cg.MontyHallSim(3)
        sim.init_doors(3)
        sim.picked = np.arange(9).reshape((3, 3))
        new = sim.select(x=2, y=None, copy=True)
        assert (new.picked.sum() == 6 + 7 + 8)

    @pytest.mark.filterwarnings('ignore:Non-binary')
    def test_select_multiple_trials(self):
        sim = cg.MontyHallSim(3)
        sim.init_doors(3)
        sim.picked = np.arange(9).reshape((3, 3))
        new = sim.select(x=[0, 2], y=None, copy=True)
        assert (new.picked.sum() == 0 + 1 + 2 + 6 + 7 + 8)

    @pytest.mark.filterwarnings('ignore:Non-binary')
    def test_select_multiple_trials_and_doors(self):
        sim = cg.MontyHallSim(3)
        sim.init_doors(3)
        sim.picked = np.arange(9).reshape((3, 3))
        new = sim.select(x=[0, 2], y=[0, 1], copy=True)
        assert (new.picked.sum() == 0 + 1 + 6 + 7)

    @pytest.mark.filterwarnings('ignore:Non-binary')
    def test_select_single_trial_and_door(self):
        sim = cg.MontyHallSim(3)
        sim.init_doors(3)
        sim.picked = np.arange(9).reshape((3, 3))
        new = sim.select(x=0, y=2, copy=True)
        assert (new.picked.sum() == 2)
