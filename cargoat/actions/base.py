#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base parent class for all actions.
"""

class MontyHallAction:

    def __call__(self):
        raise NotImplementedError("MontyHallActions must implement a __call__ on "
                                  "MontyHallSims.")
