#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 22:23:37 2023

@author: earnestt1234
"""

import numpy as np
import pytest

import cargoat as cg
from cargoat.arrayops import (get_index_success,
                              n_per_row,
                              one_per_row,
                              one_per_row_weighted)

class TestGetIndexSuccess:

    def make_array(self):
        a = np.full((3, 3), False)
        a[1, 1] = True
        a[2, 2] = True
        return a

    def test_standard_first(self):
        a = self.make_array()
        assert tuple(get_index_success(a, 0)) == (1, 1)

    def test_standard_notfirst(self):
        a = self.make_array()
        assert tuple(get_index_success(a, 1)) == (2, 2)

    def test_out_of_bounds(self):
        a = self.make_array()
        with pytest.raises(IndexError):
            assert get_index_success(a, 2)

class TestNPerRow:

    def test_standard(self):
        a = n_per_row((3, 3), 2, allowed=None)
        assert np.all(a.sum(axis=1) == 2)

    def test_allowed_with_room(self):
        allowed = np.full((3, 3), True)
        allowed[:, 2] = False
        a = n_per_row((3, 3), 2, allowed=allowed)
        assert np.all(a.sum(axis=1) == 2)

    def test_allowed_no_room(self):
        allowed = np.full((3, 3), True)
        allowed[:, [1, 2]] = False
        a = n_per_row((3, 3), 2, allowed=allowed)
        assert np.all(a.sum(axis=1) == 1)

    def test_allowed_no_room_no_enforce(self):
        allowed = np.full((3, 3), True)
        allowed[:, [1, 2]] = False
        a = n_per_row((3, 3), 2, allowed=allowed, enforce_allowed=False)
        assert np.all(a.sum(axis=1) == 2)

class TestOnePerRow:

    def test_standard(self):
        a = one_per_row((3, 3), allowed=None)
        assert np.all(a.sum(axis=1) == 1)

    def test_allowed_with_room(self):
        a = one_per_row((3, 3), allowed=None)
        allowed = np.full((3, 3), True)
        allowed[:, 2] = False
        assert np.all(a.sum(axis=1) == 1)

    def test_allowed_no_room(self):
        allowed = np.full((3, 3), False)
        a = one_per_row((3, 3), allowed=allowed)
        assert np.all(a.sum(axis=1) == 0)

    def test_allowed_no_room_no_enforce(self):
        allowed = np.full((3, 3), False)
        a = one_per_row((3, 3), allowed=allowed, enforce_allowed=False)
        assert np.all(a.sum(axis=1) == 1)

class TestOnePerRowWeighted:

    def test_certain_door(self):
        a = one_per_row_weighted((3, 3), weights=[1, 0, 0])
        exp = np.array([[1, 0, 0],
                        [1, 0, 0],
                        [1, 0, 0]])
        assert np.all(a == exp)

    def test_even_weights(self):
        a = one_per_row_weighted((3, 3), weights=[1, 1, 1])
        assert np.all(a.sum(axis=1) == 1)

    def test_allowed_full_weights(self):
        allowed = np.full((3, 3), True)
        allowed[:, 2] = False
        a = one_per_row_weighted((3, 3), weights=[1, 1, 1], allowed=allowed)
        assert np.all(a.sum(axis=1) == 1) and a[:, 2].sum() == 0

    def test_allowed_less_weights(self):
        allowed = np.full((3, 3), True)
        allowed[:, 2] = False
        a = one_per_row_weighted((3, 3), weights=[1, 1], allowed=allowed)
        assert np.all(a.sum(axis=1) == 1) and a[:, 2].sum() == 0

    def test_too_few_weights(self):
        allowed = np.full((3, 3), True)
        allowed[:, 2] = False
        with pytest.raises(ValueError):
            one_per_row_weighted((3, 3), weights=[1], allowed=allowed)

    def test_zero_weights(self):
        with pytest.raises(ValueError):
            one_per_row_weighted((3, 3), weights=[0, 0, 0])

    def test_row_unallowed(self):
        allowed = np.full((3, 3), True)
        allowed[0, :] = False
        with pytest.raises(ValueError):
            one_per_row_weighted((3, 3), weights=[1, 1, 1], allowed=allowed)
