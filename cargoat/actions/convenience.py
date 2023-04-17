#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Actions which are convenient but mostly redundant with other methods.
"""

from cargoat.actions.base import MontyHallAction
from cargoat.actions.pick import Pick

class Pass(MontyHallAction):
    '''Action for doing nothing.'''
    def __call__(self, sim):
        return sim

class Stay(MontyHallAction):
    '''Model the action of keeping the same door in the Monty
    Hall game, as opposed to switching.  Action is equivalent
    to `Pass`, aka doing nothing.'''
    def __call__(self, sim):
        return sim

class Switch(MontyHallAction):
    '''Model the action of switching doors in the Monty Hall game
    (traditionally, after one goat has been revealed).  This
    is equivalent to picking a new door, implement with
    `cg.actions.pick.Pick`.'''
    def __init__(self):
        self.action = Pick()

    def __call__(self, sim):
        return self.action(sim)
