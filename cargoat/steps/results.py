#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 12:26:23 2022

@author: earnestt1234
"""

import pprint

class Finish:
    def __call__(self, sim):
        pprint.pprint(sim.get_results(), sort_dicts=False)
