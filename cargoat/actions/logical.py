#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes for logical combination of other actions.
"""

from cargoat.actions.convenience import Pass
from cargoat.actions.base import MontyHallAction
from cargoat.sim import combine_sims

import numpy as np

class ChanceTo(MontyHallAction):
    def __init__(self, p, action):
        '''
        Class for doing a certain action with a given probability.
        A random number is used to decide what proportion of trials in
        the simulation will have the action applied.

        Parameters
        ----------
        p : float
            Probability of applying the action.
        action : cargoat.actions.base.MontyHallAction
            Monty Hall game action.

        Returns
        -------
        None.

        '''
        self.p = p
        self.action = action

    def __call__(self, sim):
        draws = np.random.rand(len(sim.idx))
        action = IfElse(draws < self.p, self.action, Pass(), call=False)
        action(sim)
        return sim

class IfElse(MontyHallAction):
    def __init__(self, condition, a, b, call=True):
        '''
        Do an if-else comparison to decide which of two actions
        to apply.  A condition is tested on all rows of the simulation
        (or otherwise a precomputed condition is provided); rows corresponding
        to `True` have one action applied, those corresponding to `False`
        have a different action applied.

        Parameters
        ----------
        condition :  callable or list-like
            Evaluation condition.  By default, this is expected to be
            a callable.  The callable is passed the current simulation,
            and is expected to return a boolean 1D array which dictates
            the rows to apply action `a` to.

            A pre-computed condition can be applied by passing `call=False` -
            in this case, `condition` will not be called, it will simply
            be used to decide how to apply actions `a` and `b`.
        a : cargoat.actions.base.MontyHallAction
            Action to apply if True.
        b : cargoat.actions.base.MontyHallAction
            Action to apply if False.
        call : bool, optional
            Treat `condition` as a callable. The default is True.

        Returns
        -------
        None.

        '''
        self.condition = condition
        self.a = a
        self.b = b
        self.call = call

    def __call__(self, sim):

        bools = self.condition(sim) if self.call else self.condition
        sim_true = sim.select(x=bools)
        sim_false = sim.select(x=~bools)
        sim_true._ifelse_index = bools
        sim_false._ifelse_index = ~bools

        self.a(sim_true)
        self.b(sim_false)

        index = (~bools).astype(int)
        new = combine_sims([sim_true, sim_false], index=index)

        sim.picked = new.picked
        sim.revealed = new.revealed
        sim.cars = new.cars
        sim.spoiled = new.spoiled

        return sim

class TryExcept(MontyHallAction):
    def __init__(self, a, b):
        '''
        Try to apply one action; if that produces errors, apply a different
        action.

        **Note that this is a try/except for all rows of the simulation -
        the error handling is not tested rowwise**.  So if action `a` fails
        for *any* trial, action `b` will be instead applied to *all* trials.
        A temporary copy simulation is created to save the state prior to
        applying action `a`.

        Parameters
        ----------
        a : cargoat.actions.base.MontyHallAction
            Action to try.
        b : cargoat.actions.base.MontyHallAction
            Action to apply if `a` raises an error.

        Returns
        -------
        None.

        '''
        self.a = a
        self.b = b

    def __call__(self, sim):
        temp = sim.copy()
        try:
            self.a(sim)
        except:
            self.b(temp)
            sim.picked=temp.picked
            sim.cars=temp.cars
            sim.revealed=temp.revealed
            sim.spoiled=temp.spoiled
        finally:
            return sim
