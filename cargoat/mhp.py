#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class for `MontyHallProblem`, the general interface for creating
Monty Hall experiments.
"""

from cargoat.errors import MontyHallError
from cargoat.sim import MontyHallSim

class MontyHallProblem:
    def __init__(self, steps=None):
        steps = [] if steps is None else steps
        self.steps = steps
        self._error_sim = None

    def run(self, n):
        sim = MontyHallSim(n=n)
        for i, step in enumerate(self.steps):
            try:
                step(sim)
            except Exception as error:
                self._error_sim = sim
                msg = f'Error for step {i}: {repr(step)}'
                raise MontyHallError(msg) from error

        return sim


    def return_error_sim(self):
        return self._error_sim

