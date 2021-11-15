#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core functions for doing things in cargoat.
"""

from cargoat.errors import MontyHallError
from cargoat.sim import MontyHallSim

def simulate(steps, n=100):
    sim = MontyHallSim(n=n)
    for i, step in enumerate(steps):
        try:
            step(sim)
        except Exception as error:
            msg = f'Error for step {i}: {repr(step)}'
            raise MontyHallError(msg) from error

    return sim