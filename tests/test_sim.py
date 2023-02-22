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

# ---- Helpers
def generate_all_one_door_sims():
    sims = []
    opts = [True, False]
    for i in opts:
        for j in opts:
            for k in opts:
                sim = cg.MontyHallSim(1)
                sim.init_doors(1)
                if i:
                    sim.cars[0, 0] = 1
                if j:
                    sim.picked[0, 0] = 1
                if k:
                    sim.revealed[0, 0] = 1
                sims.append(sim)

    return sims

# ---- Main Testing

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

class TestSimEqual:

    def test_copy_equal(self):
        a = cg.MontyHallSim(5)
        a.init_doors(3)
        b = a.copy()
        assert a == b

    @pytest.mark.parametrize("target", all_arrays)
    def test_one_door_changed(self, target):
        a = cg.MontyHallSim(5)
        a.init_doors(3)
        b = a.copy()
        if target == 'spoiled':
            b.spoiled[0] = 1
        else:
            getattr(b, target)[0, 0] = 1
        assert a != b

    def test_empty_equal_same_n(self):
        a = cg.MontyHallSim(10)
        b = cg.MontyHallSim(10)
        assert a == b

    def test_empty_equal_diff_n(self):
        a = cg.MontyHallSim(10)
        b = cg.MontyHallSim(5)
        assert a != b

    def test_constructed_separately(self):
        a = cg.MontyHallSim(3)
        a.init_doors(3)
        a.picked[1, 1] = 1

        b = cg.MontyHallSim(3)
        b.init_doors(3)
        b.picked[1, 1] = 1

        assert a == b

    def test_non_sim_other(self):
        a = cg.MontyHallSim(10)
        b = dict()
        assert (a != b) and (b != a)

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


class TestSetArrayOneDoor:

    @pytest.mark.parametrize("sim", generate_all_one_door_sims())
    @pytest.mark.parametrize("target", main_arrays)
    @pytest.mark.parametrize("behavior", ['overwrite', 'add', 'remove'])
    @pytest.mark.parametrize("allow_spoiled", [True, False])
    def test_set_array(self, sim, target, behavior, allow_spoiled):

        allow_spoiled = False

        def setter(sim, new_array):
            sim._set_array(target=target, new_array=new_array,
                           behavior=behavior, allow_spoiled=allow_spoiled,
                           allow_redundant=True)

        SUCCESS = False

        new_array = np.ones([1, 1], dtype=int)
        check_spoiled = sim._get_spoiling_func(target)
        valid = check_spoiled(new_array, behavior=behavior, allow_spoiled=True)
        should_spoil = not valid[0, 0]
        spoil_etype = {'cars': BadCar,
                       'revealed': BadReveal,
                       'picked': BadPick}[target]

        if should_spoil and not allow_spoiled:
            try:
                setter(sim, new_array)
            except spoil_etype:
                SUCCESS = True

        elif should_spoil and allow_spoiled:
            setter(sim, new_array)
            if sim.spoiled[0] == 1:
                SUCCESS = True

        else:
            setter(sim, new_array)
            answer = 1 if behavior in ['add', 'overwrite'] else 0
            SUCCESS = getattr(sim, target)[0, 0] == answer

        assert SUCCESS

class TestApplyFunc:

    def make_sim(self):
        sim = cg.MontyHallSim(3)
        sim.init_doors(3)
        return sim

    def test_not_inplace_correct(self):
        sim = self.make_sim()
        func = lambda x: x + 42
        sim.apply_func(func, inplace=False)
        assert [(getattr(sim, target) == 42).all()
                for target in main_arrays]

    def test_not_inplace_incorrect(self):
        sim = self.make_sim()
        func = lambda x: x + 42
        sim.apply_func(func, inplace=True)
        assert [(getattr(sim, target) == 0).all()
                for target in main_arrays]

    def test_inplace_correct(self):
        sim = self.make_sim()
        func = lambda x: np.place(x, x==0, 42)
        sim.apply_func(func, inplace=True)
        assert [(getattr(sim, target) == 42).all()
                for target in main_arrays]

    def test_inplace_incorrect(self):
        sim = self.make_sim()
        func = lambda x: np.place(x, x==0, 42)
        sim.apply_func(func, inplace=False)
        assert [(getattr(sim, target) is None)
                for target in main_arrays]

    def test_none_specified(self):
        sim = self.make_sim()
        func = lambda x: x + 42
        sim.apply_func(func, inplace=False, cars=False, picked=False, revealed=False)
        assert [(getattr(sim, target) == 0).all()
                for target in main_arrays]

class TestCopy:

    def test_copy_empty(self):
        a = cg.MontyHallSim(10)
        b = a.copy()
        assert b.empty

    def test_copy_full(self):
        a = cg.MontyHallSim(3)
        a.init_doors(3)
        a.cars[:] = 1
        a.picked[:] = 1
        a.revealed[:] = 1
        a.spoiled[:] = 1

        b = a.copy()
        assert all([np.all(b.cars == 1),
                    np.all(b.picked == 1),
                    np.all(b.revealed == 1),
                    np.all(b.spoiled == 1)])

class TestGetResults:

    def make_sim(self):
        # first 5 trials have car in door 0
        # last 5 trials have car in door 2
        sim = cg.MontyHallSim(10)
        sim.init_doors(3)
        sim.cars[:5, 0] = 1
        sim.cars[5:, 2] = 1

        return sim

    def make_sim_spoiled(self):
        # same as above, but mark doors 0-5 as spoiled
        sim = self.make_sim()
        sim.spoiled[:5] = 1

        return sim

    def test_expected_keys(self):
        sim = self.make_sim()
        r = sim.get_results()
        assert set(r.keys()) == {'wins', 'losses', 'trials', 'percent_wins', 'percent_losses'}

    def test_wins_none_picked(self):
        sim = self.make_sim()
        r = sim.get_results(spoiled_games='omit')
        assert r['wins'] == 0

    def test_wins_all_picked(self):
        sim = self.make_sim()
        sim.picked[:5, 0] = 1
        sim.picked[5:, 2] = 1
        r = sim.get_results(spoiled_games='omit')
        assert r['wins'] == 10

    def test_wins_half_picked(self):
        sim = self.make_sim()
        sim.picked[:, 0] = 1
        r = sim.get_results(spoiled_games='omit')
        assert r['wins'] == 5

    def test_wins_overpicked(self):
        sim = self.make_sim()
        sim.picked[:] = 1
        r = sim.get_results(spoiled_games='omit')
        assert r['wins'] == 10

    def test_wins_omit_spoiled(self):
        sim = self.make_sim_spoiled()
        sim.picked = sim.cars
        r = sim.get_results(spoiled_games='omit')
        assert (r['wins'] == 5) and (r['percent_wins'] == 100)

    def test_wins_include_spoiled(self):
        sim = self.make_sim_spoiled()
        sim.picked = sim.cars
        r = sim.get_results(spoiled_games='include')
        assert (r['wins'] == 10) and (r['percent_wins'] == 100)

    def test_wins_only_spoiled(self):
        sim = self.make_sim_spoiled()
        sim.picked = sim.cars
        r = sim.get_results(spoiled_games='only')
        assert (r['wins'] == 5) and (r['percent_wins'] == 100)

class TestCombineSims:

    def make_sims(self):
        a = cg.MontyHallSim(3)
        a.init_doors(3)
        a.picked[:] = 1

        b = cg.MontyHallSim(3)
        b.init_doors(3)

        return a, b

    def test_no_index(self):
        a, b = self.make_sims()
        c = cg.combine_sims([a, b])
        picked = np.array([[1, 1, 1],
                           [1, 1, 1],
                           [1, 1, 1],
                           [0, 0, 0],
                           [0, 0, 0],
                           [0, 0, 0]])

        assert np.all(c.picked == picked)

    def test_interleave(self):
        a, b = self.make_sims()
        c = cg.combine_sims([a, b], index=[0, 1, 0, 1, 0, 1])
        picked = np.array([[1, 1, 1],
                           [0, 0, 0],
                           [1, 1, 1],
                           [0, 0, 0],
                           [1, 1, 1],
                           [0, 0, 0]])

        assert np.all(c.picked == picked)

    def test_index_out_of_bounds(self):
        a, b = self.make_sims()
        with pytest.raises(IndexError):
            _ = cg.combine_sims([a, b], index=[1, 2, 1, 2, 1, 2])

    def test_index_wrong_length(self):
        a, b = self.make_sims()
        with pytest.raises(ValueError):
            _ = cg.combine_sims([a, b], index=[0, 1])

    def test_combine_wrong_shape(self):
        a, _ = self.make_sims()
        b = cg.MontyHallSim(3)
        b.init_doors(5)
        with pytest.raises(ValueError):
            _ = cg.combine_sims([a, b])

    def test_empty_sim(self):
        a, _ = self.make_sims()
        b = cg.MontyHallSim(3)
        with pytest.raises(ValueError):
            _ = cg.combine_sims([a, b])
