#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 23:00:59 2022

@author: earnestt1234
"""

import itertools as it

import numpy as np
import pytest

import cargoat as cg
from cargoat.errors import BadCar, BadPick, BadReveal

main_arrays = ['cars', 'revealed', 'picked']
main_etypes = [cg.errors.BadCar, cg.errors.BadReveal, cg.errors.BadPick]
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

    def test_no_copy(self):
        sim = cg.MontyHallSim(3)
        sim.init_doors(3)
        new = sim.select(x=None, y=None, copy=False)
        new.picked[0, 0] = 42
        assert (sim.picked[0, 0] == 42)

    def test_copy(self):
        sim = cg.MontyHallSim(3)
        sim.init_doors(3)
        new = sim.select(x=None, y=None, copy=True)
        new.picked[0, 0] = 42
        assert (sim.picked[0, 0] == 0)

    @pytest.mark.filterwarnings('ignore:Non-binary')
    def test_boolean_x(self):
        sim = cg.MontyHallSim(3)
        sim.init_doors(3)
        sim.picked = np.arange(9).reshape((3, 3))
        new = sim.select(x=[True, False, True], y=None, copy=True)
        assert (new.picked.sum() == 0 + 1 + 2 + 6 + 7 + 8)

    @pytest.mark.filterwarnings('ignore:Non-binary')
    def test_boolean_y(self):
        sim = cg.MontyHallSim(3)
        sim.init_doors(3)
        sim.picked = np.arange(9).reshape((3, 3))
        new = sim.select(x=None, y=[True, False, True], copy=True)
        assert (new.picked.sum() == 0 + 3 + 6 + 2 + 5 + 8)

    @pytest.mark.filterwarnings('ignore:Non-binary')
    def test_boolean_both(self):
        sim = cg.MontyHallSim(3)
        sim.init_doors(3)
        sim.picked = np.arange(9).reshape((3, 3))
        new = sim.select(x=[True, False, True], y=[True, False, True], copy=True)
        assert (new.picked.sum() == 0 + 6 + 2 + 8)

class TestSimStatusFuncs:

    def generate_pickable_sim(self):
        sim = cg.MontyHallSim(3)
        sim.init_doors(3)
        sim.picked = np.identity(3, dtype=int)
        return sim

    def generate_revealable_sim(self):
        sim = cg.MontyHallSim(3)
        sim.init_doors(4)
        sim.cars[:, 0] = 1
        sim.picked[:, 1] = 1
        sim.revealed[:, 2] = 1
        return sim

    def test_pickable_doors_exlcude_current(self):
        sim = self.generate_pickable_sim()
        pickable = np.array([[0, 1, 1],
                           [1, 0, 1],
                           [1, 1, 0]]).astype(bool)
        assert (sim.pickable_doors(exclude_current=True) == pickable).all()

    def test_pickable_doors_not_exlcude_current(self):
        sim = self.generate_pickable_sim()
        pickable = np.array([[1, 1, 1],
                           [1, 1, 1],
                           [1, 1, 1]]).astype(bool)
        assert (sim.pickable_doors(exclude_current=False) == pickable).all()

    def test_query_doors_or_all_combos(self):
        sim = cg.MontyHallSim(3)
        sim.init_doors(3)
        sim.cars[:, 0] = 1
        sim.picked[:, 1] = 1
        sim.revealed[:, 2] = 1

        names = ['cars', 'picked', 'revealed',
                 'not_cars', 'not_picked', 'not_revealed']

        def _validate_query(query, cars=False, picked=False, revealed=False,
                            not_cars=False, not_picked=False, not_revealed=False):
            bools = []
            if cars:
                bools.append(query[:, 0].all())
            if picked:
                bools.append(query[:, 1].all())
            if revealed:
                bools.append(query[:, 2].all())
            if not_cars:
                bools.append(query[:, [1, 2]].all())
            if not_picked:
                bools.append(query[:, [0, 2]].all())
            if not_revealed:
                bools.append(query[:, [0, 1]].all())

            return all(bools)

        validations = []

        for bools in it.product((True, False), repeat=6):
            args = dict(zip(names, bools))
            query = sim.query_doors_or(**args)
            ans = _validate_query(query, **args)
            validations.append(ans)

        assert(all(validations))

    def test_revealable_doors(self):
        sim = self.generate_revealable_sim()
        revealable = sim.revealable_doors()
        answer = np.zeros([3, 4], dtype=int)
        answer[:, 3] = 1
        assert (revealable == answer).all()

class TestSimSetArray:

    def generate_blank_sim(self):
        sim = cg.MontyHallSim(5)
        sim.init_doors(3)
        return sim

    @pytest.mark.parametrize("target", main_arrays)
    def test_wrong_shape(self, target):
        sim = self.generate_blank_sim()
        new = np.zeros([4, 4], dtype=int)
        with pytest.raises(ValueError):
            sim._set_array(target, new)

    @pytest.mark.parametrize("i", [0, 1, 2])
    def test_wrong_n_per_row(self, i):
        target = main_arrays[i]
        etype = main_etypes[i]
        sim = self.generate_blank_sim()
        new = np.zeros(sim.shape, dtype=int)
        with pytest.raises(etype):
            sim._set_array(target, new, n_per_row=1)

    @pytest.mark.parametrize("i", [0, 1, 2])
    def test_okay_n_per_row(self, i):
        target = main_arrays[i]
        sim = self.generate_blank_sim()
        new = np.ones(sim.shape, dtype=int)
        sim._set_array(target, new, n_per_row=3)
        assert (getattr(sim, target).sum() == np.prod(sim.shape))

    @pytest.mark.parametrize("i", [0, 1, 2])
    def test_redundant_allowed(self, i):
        target = main_arrays[i]
        sim = self.generate_blank_sim()
        a = getattr(sim, target)
        a[:, 0] = 1
        new = a.copy()
        sim._set_array(target, new, allow_redundant=True)
        assert (getattr(sim, target).sum() == sim.shape[0])

    @pytest.mark.parametrize("i", [0, 1, 2])
    def test_redundant_not_allowed(self, i):
        target = main_arrays[i]
        etype = main_etypes[i]
        sim = self.generate_blank_sim()
        a = getattr(sim, target)
        a[:, 0] = 1
        new = a.copy()

        with pytest.raises(etype):
            sim._set_array(target, new, allow_redundant=False)

    @pytest.mark.parametrize("i", [0, 1, 2])
    def test_add(self, i):
        target = main_arrays[i]
        sim = self.generate_blank_sim()
        a = getattr(sim, target)
        rows = sim.shape[0]
        first_half = rows // 2
        last_half = rows - first_half
        a[:first_half, -1] = 0
        a[:last_half, -1] = 1

        new_array = np.zeros(sim.shape, dtype=int)
        new_array[:, -1] = 1
        sim._set_array(target, new_array, behavior='add')

        assert(all(getattr(sim, target)[:, -1] == 1))

    @pytest.mark.parametrize("i", [0, 1, 2])
    def test_overwrite(self, i):
        target = main_arrays[i]
        sim = self.generate_blank_sim()
        new_array = np.ones(sim.shape, dtype=int)
        sim._set_array(target, new_array, behavior='overwrite')

        assert np.all(getattr(sim, target) == 1)

class TestSetArraySpoiling:

    def generate_ordered_coloumn_sim(self):
        n = 5
        sim = cg.MontyHallSim(n)
        sim.init_doors(4)
        sim.cars[:, 1] = 1
        sim.picked[:, 2] = 1
        sim.revealed[:, 3] = 1
        return sim

    def ordered_sim_setter_helper(self, target, behavior,
                                  allow_spoiled, should_spoil=None,
                                  spoil_etype=None):

        def setter(sim, new_array):
            sim._set_array(target=target, new_array=new_array,
                           behavior=behavior, allow_spoiled=allow_spoiled)

        trials = []
        sim = self.generate_ordered_coloumn_sim()
        rows, columns = sim.shape

        if should_spoil is None:
            should_spoil = lambda x : np.full((rows, columns), False)

        for i in range(columns):
            CORRECT = False
            sim = self.generate_ordered_coloumn_sim()
            new_array = np.zeros(sim.shape, dtype=int)
            new_array[:, i] = 1

            expect_spoil_doors = should_spoil(sim)
            if any(expect_spoil_doors[:, i]) and not allow_spoiled:
                try:
                    setter(sim, new_array)
                except spoil_etype:
                    CORRECT = True

            elif any(expect_spoil_doors[:, i]) and allow_spoiled:
                setter(sim, new_array)
                if all(expect_spoil_doors[:, i] == sim.spoiled):
                    CORRECT = True

            else:
                setter(sim, new_array)
                CORRECT = True

            trials.append(CORRECT)

        assert all(trials) and len(trials) == columns

    def test_pick_overwrite_not_allowed(self):

        should_spoil = lambda x: x.revealed.astype(bool)
        self.ordered_sim_setter_helper(target='picked',
                                       behavior='overwrite',
                                       allow_spoiled=False,
                                       should_spoil=should_spoil,
                                       spoil_etype=BadPick)

    def test_pick_overwrite_allowed(self):

        should_spoil = lambda x: x.revealed.astype(bool)
        self.ordered_sim_setter_helper(target='picked',
                                       behavior='overwrite',
                                       allow_spoiled=True,
                                       should_spoil=should_spoil,
                                       spoil_etype=BadPick)



