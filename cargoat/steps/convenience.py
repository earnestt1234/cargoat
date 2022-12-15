#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Steps which are convenient but mostly redundant with other methods.
"""

from cargoat.steps.pick import Pick

class Pass:
    '''Step for doing nothing.'''
    def __call__(self, sim):
        pass

class Stay:
    '''Model the action of keeping the same door in the Monty
    Hall game, as opposed to switching.  Action is equivalent
    to `Pass`, aka doing nothing.'''
    def __call__(self, sim):
        pass

class Switch:
    '''Model the action of switching doors in the Monty Hall game
    (traditionally, after one goat has been revealed).  This
    is equivalent to picking a new door, implement with
    `cg.steps.pick.Pick`.'''
    def __init__(self):
        self.action = Pick()

    def __call__(self, sim):
        self.action(sim)
