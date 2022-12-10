#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 14:59:27 2022

@author: earnestt1234
"""

from cargoat.steps.pick import Pick

class Pass:
    def __call__(self, sim):
        pass

class Stay:
    def __call__(self, sim):
        pass

class Switch:
    def __init__(self):
        self.action = Pick()

    def __call__(self, sim):
        self.action(sim)
